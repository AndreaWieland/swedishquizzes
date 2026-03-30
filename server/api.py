import json
import random
import uuid
import importlib
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

TOPICS_DIR = Path(__file__).parent / "topics"
STATS_DIR = Path(__file__).parent / "stats"
PROGRESS_DIR = Path(__file__).parent / "progress"

app = FastAPI(
    title="Swedish Vocabulary Quiz API",
    description="REST API for quizzing Swedish vocabulary with adaptive weighting.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pending questions keyed by question_id, holding correct answer + metadata.
# In-memory only; lost on restart (which is fine — client just requests a new question).
_pending: dict[str, dict] = {}


# ---------------------------------------------------------------------------
#  Data helpers
# ---------------------------------------------------------------------------

def _topic_names() -> list[str]:
    return sorted(
        p.stem for p in TOPICS_DIR.glob("*.py") if p.name != "__init__.py"
    )


def _require_topic(name: str) -> str:
    if name not in _topic_names():
        raise HTTPException(404, f"Topic '{name}' not found")
    return name


def _load_topic(name: str) -> dict:
    mod = importlib.import_module(f"topics.{name}")
    return {
        "nouns": getattr(mod, "nouns", []),
        "verbs": getattr(mod, "verbs", []),
        "misc": getattr(mod, "misc", []),
    }


def _normalize_misc(entry: dict) -> dict:
    """Ensure misc entries always expose a 'swedish' key."""
    if "swedish" not in entry and "word" in entry:
        out = dict(entry)
        out["swedish"] = out.pop("word")
        return out
    return entry


def _swedish_key(entry: dict) -> Optional[str]:
    for f in ("indefinite", "infinitive", "swedish", "word"):
        if f in entry:
            return entry[f]
    return None


def _word_key(entry: dict) -> str:
    """Stable unique key for any word entry (noun/verb/misc)."""
    if "indefinite" in entry:
        return f"noun-{entry['indefinite']}"
    if "infinitive" in entry:
        return f"verb-{entry['infinitive']}"
    sw = entry.get("swedish", entry.get("word"))
    return f"misc-{sw}"


def _word_type(entry: dict) -> str:
    if "indefinite" in entry:
        return "noun"
    if "infinitive" in entry:
        return "verb"
    return "misc"


def _sort_key_for_learning(entry: dict):
    """CEFR ascending, then frequency descending — learn common easy words first."""
    cefr = entry.get("cefr", 99)
    freq = entry.get("frequency") or 0
    return (cefr, -freq)


# ---------------------------------------------------------------------------
#  Stats persistence
# ---------------------------------------------------------------------------

def _load_stats(topic: str) -> dict:
    p = STATS_DIR / f"{topic}_stats.json"
    if p.exists():
        return json.loads(p.read_text("utf-8"))
    return {}


def _save_stats(topic: str, stats: dict):
    STATS_DIR.mkdir(exist_ok=True)
    p = STATS_DIR / f"{topic}_stats.json"
    p.write_text(json.dumps(stats, ensure_ascii=False, indent=2), "utf-8")


# ---------------------------------------------------------------------------
#  Progress persistence (learned words)
# ---------------------------------------------------------------------------

def _load_learned(topic: str) -> set[str]:
    p = PROGRESS_DIR / f"{topic}.json"
    if p.exists():
        return set(json.loads(p.read_text("utf-8")))
    return set()


def _save_learned(topic: str, learned: set[str]):
    PROGRESS_DIR.mkdir(exist_ok=True)
    p = PROGRESS_DIR / f"{topic}.json"
    p.write_text(json.dumps(sorted(learned), ensure_ascii=False, indent=2), "utf-8")


def _all_words_flat(data: dict) -> list[dict]:
    """Return all words from a topic as a flat list."""
    return data["nouns"] + data["verbs"] + data["misc"]


# ---------------------------------------------------------------------------
#  Adaptive weighting (ported from CLI trainer)
# ---------------------------------------------------------------------------

def _weight(stats: dict, key: str) -> float:
    rec = stats.get(key, {"asked": 0, "correct": 0})
    if rec["asked"] == 0:
        return 4.0
    accuracy = rec["correct"] / rec["asked"]
    return max(0.5, 4.0 * (1 - accuracy))


# ---------------------------------------------------------------------------
#  Question generators
# ---------------------------------------------------------------------------

def _noun_question(noun: dict, all_nouns: list, stats: dict) -> dict:
    forms = ["indefinite", "definite", "plural", "plural_definite"]
    form = random.choice(forms)
    direction = random.choice(["to_english", "to_swedish"])
    stat_key = f"noun-{noun['indefinite']}-{form}"
    swedish_form = noun.get(form, noun["indefinite"])

    q: dict = {
        "type": "noun",
        "form": form,
        "direction": direction,
        "word": noun,
        "stat_key": stat_key,
    }

    if direction == "to_english":
        correct = noun["english"]
        pool = [n["english"] for n in all_nouns if n["english"] != correct]
        wrong = random.sample(pool, k=min(3, len(pool)))
        options = wrong + [correct]
        random.shuffle(options)
        q["prompt"] = f"What is the English meaning of '{swedish_form}'?"
        q["options"] = options
        q["_correct"] = correct
    else:
        q["prompt"] = f"What is the {form.replace('_', ' ')} form of '{noun['english']}'?"
        q["_correct"] = swedish_form

    return q


def _verb_question(verb: dict, stats: dict) -> dict:
    tenses = [t for t in ("present", "past", "supine", "imperative") if t in verb]
    tense = random.choice(tenses) if tenses else "present"
    stat_key = f"verb-{verb['infinitive']}-{tense}"

    direction = random.choice(["hint_swedish", "from_english"])
    q: dict = {
        "type": "verb",
        "tense": tense,
        "direction": direction,
        "word": verb,
        "stat_key": stat_key,
        "_correct": verb[tense],
    }

    if direction == "hint_swedish":
        q["prompt"] = (
            f"What is the {tense} form of '{verb['infinitive']}' "
            f"({verb['english']})?"
        )
    else:
        q["prompt"] = f"What is the {tense} form of '{verb['english']}'?"

    return q


def _misc_question(entry: dict, all_misc: list, stats: dict) -> dict:
    entry = _normalize_misc(entry)
    swedish = entry["swedish"]
    direction = random.choices(
        ["to_english", "to_swedish"], weights=[0.3, 0.7], k=1
    )[0]
    stat_key = f"misc-{swedish}"

    q: dict = {
        "type": "misc",
        "direction": direction,
        "word": entry,
        "stat_key": stat_key,
    }

    if direction == "to_english":
        correct = entry["english"]
        pool = [
            _normalize_misc(m)["english"]
            for m in all_misc
            if _normalize_misc(m)["english"] != correct
        ]
        wrong = random.sample(pool, k=min(3, len(pool)))
        options = wrong + [correct]
        random.shuffle(options)
        q["prompt"] = f"What does '{swedish}' mean?"
        q["options"] = options
        q["_correct"] = correct
    else:
        q["prompt"] = f"How do you say '{entry['english']}' in Swedish?"
        q["_correct"] = swedish

    return q


# ---------------------------------------------------------------------------
#  Routes — Topics
# ---------------------------------------------------------------------------

@app.get("/topics", tags=["topics"])
def list_topics():
    """List all available topics with word counts."""
    topics = []
    for name in _topic_names():
        data = _load_topic(name)
        n, v, m = len(data["nouns"]), len(data["verbs"]), len(data["misc"])
        topics.append({
            "name": name,
            "display_name": name.replace("_", " ").title(),
            "counts": {"nouns": n, "verbs": v, "misc": m, "total": n + v + m},
        })
    return {"topics": topics}


@app.get("/topics/{topic}", tags=["topics"])
def get_topic_words(topic: str):
    """Return every word in a topic, organised by type."""
    _require_topic(topic)
    data = _load_topic(topic)
    return {
        "topic": topic,
        "nouns": data["nouns"],
        "verbs": data["verbs"],
        "misc": [_normalize_misc(m) for m in data["misc"]],
    }


# ---------------------------------------------------------------------------
#  Routes — Quiz
# ---------------------------------------------------------------------------

@app.get("/quiz", tags=["quiz"])
def get_question(topic: str = Query(..., description="Topic name to quiz on")):
    """Get a weighted-random quiz question. Only quizzes words that have been learned."""
    _require_topic(topic)
    data = _load_topic(topic)
    stats = _load_stats(topic)
    learned = _load_learned(topic)

    pool: list[tuple[str, dict, float]] = []
    for noun in data["nouns"]:
        if _word_key(noun) in learned:
            pool.append(("noun", noun, _weight(stats, f"noun-{noun['indefinite']}")))
    for verb in data["verbs"]:
        if _word_key(verb) in learned:
            pool.append(("verb", verb, _weight(stats, f"verb-{verb['infinitive']}")))
    for misc in data["misc"]:
        if _word_key(misc) in learned:
            sw = _swedish_key(misc)
            pool.append(("misc", misc, _weight(stats, f"misc-{sw}")))

    if not pool:
        raise HTTPException(
            404,
            "No learned words in this topic yet. Use POST /learn to learn some first.",
        )

    (wtype, entry, _) = random.choices(pool, weights=[w for _, _, w in pool], k=1)[0]

    if wtype == "noun":
        q = _noun_question(entry, data["nouns"], stats)
    elif wtype == "verb":
        q = _verb_question(entry, stats)
    else:
        q = _misc_question(entry, data["misc"], stats)

    qid = str(uuid.uuid4())
    _pending[qid] = {
        "topic": topic,
        "stat_key": q.pop("stat_key"),
        "correct": q.pop("_correct"),
    }
    q["question_id"] = qid
    return q


class AnswerBody(BaseModel):
    answer: str


@app.post("/quiz/{question_id}", tags=["quiz"])
def submit_answer(question_id: str, body: AnswerBody):
    """Submit an answer for a pending question. Returns whether it was correct and the right answer."""
    if question_id not in _pending:
        raise HTTPException(404, "Question not found or already answered")

    q = _pending.pop(question_id)
    is_correct = body.answer.strip().lower() == q["correct"].strip().lower()

    stats = _load_stats(q["topic"])
    rec = stats.setdefault(q["stat_key"], {"asked": 0, "correct": 0})
    rec["asked"] += 1
    if is_correct:
        rec["correct"] += 1
    _save_stats(q["topic"], stats)

    return {
        "correct": is_correct,
        "correct_answer": q["correct"],
        "stats": rec,
    }


# ---------------------------------------------------------------------------
#  Routes — Learn
# ---------------------------------------------------------------------------

@app.post("/learn", tags=["learn"])
def learn_word(topic: str = Query(..., description="Topic name to learn from")):
    """Pull the next unlearned word, see all its forms, and add it to the quiz pool.

    Words are served in learning order: lowest CEFR first, then highest frequency.
    """
    _require_topic(topic)
    data = _load_topic(topic)
    learned = _load_learned(topic)

    all_words = sorted(_all_words_flat(data), key=_sort_key_for_learning)
    unlearned = [w for w in all_words if _word_key(w) not in learned]

    if not unlearned:
        total = len(_all_words_flat(data))
        raise HTTPException(
            404, f"All {total} words in '{topic}' have been learned."
        )

    word = unlearned[0]
    key = _word_key(word)
    learned.add(key)
    _save_learned(topic, learned)

    entry = _normalize_misc(word) if _word_type(word) == "misc" else word
    return {
        "topic": topic,
        "type": _word_type(word),
        "word_key": key,
        "word": entry,
        "progress": {
            "learned": len(learned),
            "total": len(all_words),
            "remaining": len(unlearned) - 1,
        },
    }


@app.get("/learn/status", tags=["learn"])
def learn_status(topic: str = Query(..., description="Topic name")):
    """Check how many words have been learned vs total in a topic."""
    _require_topic(topic)
    data = _load_topic(topic)
    learned = _load_learned(topic)
    total = len(_all_words_flat(data))
    return {
        "topic": topic,
        "learned": len(learned),
        "total": total,
        "remaining": total - len(learned),
    }


@app.delete("/learn/{topic}", tags=["learn"])
def reset_learn_progress(topic: str):
    """Reset all learn progress for a topic."""
    _require_topic(topic)
    _save_learned(topic, set())
    return {"message": f"Learn progress for '{topic}' reset"}


# ---------------------------------------------------------------------------
#  Routes — Stats
# ---------------------------------------------------------------------------

@app.get("/stats", tags=["stats"])
def get_all_stats():
    """Per-topic summary of quiz performance."""
    result = {}
    for name in _topic_names():
        s = _load_stats(name)
        asked = sum(r["asked"] for r in s.values())
        correct = sum(r["correct"] for r in s.values())
        result[name] = {
            "total_asked": asked,
            "total_correct": correct,
            "accuracy": round(correct / asked, 3) if asked else 0,
            "words_seen": len(s),
        }
    return {"stats": result}


@app.get("/stats/{topic}", tags=["stats"])
def get_topic_stats(topic: str):
    """Detailed stats for a single topic."""
    _require_topic(topic)
    s = _load_stats(topic)
    asked = sum(r["asked"] for r in s.values())
    correct = sum(r["correct"] for r in s.values())
    return {
        "topic": topic,
        "summary": {
            "total_asked": asked,
            "total_correct": correct,
            "accuracy": round(correct / asked, 3) if asked else 0,
            "words_seen": len(s),
        },
        "words": s,
    }


@app.delete("/stats/{topic}", tags=["stats"])
def reset_topic_stats(topic: str):
    """Reset all stats for a topic."""
    _require_topic(topic)
    _save_stats(topic, {})
    return {"message": f"Stats for '{topic}' reset"}
