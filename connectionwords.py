import json
import random
import os

STATS_FILE = "function_word_stats.json"

# Common Swedish "in-between" words: conjunctions, prepositions, adverbs, etc.
words = [
    {"swedish": "och", "english": "and"},
    {"swedish": "men", "english": "but"},
    {"swedish": "eller", "english": "or"},
    {"swedish": "eftersom", "english": "because"},
    {"swedish": "för att", "english": "in order to / because"},
    {"swedish": "så att", "english": "so that"},
    {"swedish": "så", "english": "so / then"},
    {"swedish": "därför", "english": "therefore"},
    {"swedish": "dock", "english": "however"},
    {"swedish": "också", "english": "also"},
    {"swedish": "bara", "english": "only / just"},
    {"swedish": "mycket", "english": "much / very"},
    {"swedish": "under", "english": "under / during"},
    {"swedish": "över", "english": "over / above"},
    {"swedish": "framför", "english": "in front of"},
    {"swedish": "bakom", "english": "behind"},
    {"swedish": "mellan", "english": "between"},
    {"swedish": "utan", "english": "without / but (after negative)"},
    {"swedish": "hos", "english": "at (someone’s place)"},
    {"swedish": "genom", "english": "through"},
    {"swedish": "innan", "english": "before"},
    {"swedish": "efter", "english": "after"},
    {"swedish": "på", "english": "on / at"},
    {"swedish": "i", "english": "in / inside"},
    {"swedish": "av", "english": "of / by"},
    {"swedish": "till", "english": "to / until"},
    {"swedish": "från", "english": "from"},
    {"swedish": "när", "english": "when"},
    {"swedish": "om", "english": "if / about"},
    {"swedish": "för", "english": "for / to"},
    {"swedish": "mot", "english": "against / toward"},
    {"swedish": "bland", "english": "among"},
    {"swedish": "trots", "english": "despite"},
    {"swedish": "redan", "english": "already"},
    {"swedish": "ännu", "english": "still / yet"},
    {"swedish": "aldrig", "english": "never"},
    {"swedish": "alltid", "english": "always"},
    {"swedish": "ofta", "english": "often"},
    {"swedish": "ibland", "english": "sometimes"},
    {"swedish": "snart", "english": "soon"},
    {"swedish": "kanske", "english": "maybe / perhaps"},
    {"swedish": "nästan", "english": "almost/next"},
    {"swedish": "fortfarande", "english": "still"},
    {"swedish": "här", "english": "here"},
    {"swedish": "där", "english": "there"},
    {"swedish": "hit", "english": "to here"},
    {"swedish": "dit", "english": "to there"},
    {"swedish": "hem", "english": "home (motion)"},
    {"swedish": "hemma", "english": "at home"},
    {"swedish": "borta", "english": "away / gone"},
    {"swedish": "inne", "english": "inside"},
    {"swedish": "ute", "english": "outside"},
    {"swedish": "finns", "english": "there is / there are"},
    {"swedish": "än", "english": "yet / than"},
    {"swedish": "igen", "english": "again"},
    {"swedish": "tillsammans", "english": "together"},
    {"swedish": "ensam", "english": "alone"},
    {"swedish": "däremot", "english": "on the other hand"},
    {"swedish": "dessutom", "english": "in addition / furthermore"},
    {"swedish": "fastän", "english": "although"},
    {"swedish": "även om", "english": "even though"},
    {"swedish": "således", "english": "thus"},
    {"swedish": "nämligen", "english": "namely / that is"},
    {"swedish": "till exempel", "english": "for example"},
    {"swedish": "alltså", "english": "so / that means"},
    {"swedish": "typ", "english": "like / kind of"},
    {"swedish": "ju", "english": "(as you know / indeed)"},
    {"swedish": "väl", "english": "surely / well"},
    {"swedish": "precis", "english": "exactly"},
    {"swedish": "liksom", "english": "like / sort of"},
    {"swedish": "nyss", "english": "just (recently)"},
    {"swedish": "nära", "english": "near"},
    {"swedish": "vanligt", "english": "usual"},
    {"swedish": "ovanligt", "english": "unusual"},
    {"swedish": "plötsligt", "english": "suddenly"},
    {"swedish": "lyckligtvis", "english": "luckily"},
    {"swedish": "särskilt", "english": "particularly/ especially"},
    {"swedish": "i närheten", "english": "nearby"},
    {"swedish": "illa", "english": "badly"},
    {"swedish": "senaste", "english": "recent/latest"},
    {"swedish": "istället", "english": "instead"},
    {"swedish": "vilket", "english": "which"},
    {"swedish": "både", "english": "both"},
    {"swedish": "fler", "english": "more"},
    {"swedish": "viktiga", "english": "important"},
    {"swedish": "samtidigt", "english": "simultaneously/at the same time"},
    {"swedish": "fler", "english": "next to"},
    {"swedish": "flera", "english": "several"},
    {"swedish": "nedan", "english": "below"}, #as in below on the page
    {"swedish": "endast", "english": "only"},
    {"swedish": "tidigare", "english": "previously" },
    {"swedish": "sådant", "english": "such"},
    {"swedish": "hela", "english": "whole/all"},
    {"swedish": "tidigt", "english": "early"},
    {"swedish": "någonstans", "english": "anywhere"},
    {"swedish": "för", "english": "too [adjective]"},
    {"swedish": "vanligtvis", "english": "usually"},
    {"swedish": "tillräckligt med", "english": "enough"},
    {"swedish": "förmodligen", "english": "probably"},
    # medan: while
    # varje: every/each
    # annan: other
    # imorse: this morning
    # del: part/portion
    # helt: completely
    # inom: within
    # fram: up/forward
    # enligt: according to
    # särskilt: particularly
    utom: except


]

if os.path.exists(STATS_FILE):
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)
else:
    stats = {}

# Ensure every word has an entry
for w in words:
    sw = w["swedish"]
    if sw not in stats:
        stats[sw] = {"asked": 0, "correct": 0}

def save_stats():
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def weighted_choice(words):
    """Choose words with higher weight if accuracy is low."""
    weights = []
    for w in words:
        s = stats[w["swedish"]]
        asked, correct = s["asked"], s["correct"]
        if asked == 0:
            weight = 4.0
        else:
            acc = correct / asked
            weight = max(0.5, 4.0 * (1 - acc))
        weights.append(weight)
    return random.choices(words, weights=weights, k=1)[0]

def ask_question(word):
    """Ask question: English → Swedish = typing, Swedish → English = multiple choice."""
    s = stats[word["swedish"]]
    s["asked"] += 1

    # Randomly choose direction
    direction = random.choice(["to_english", "to_swedish"])

    if direction == "to_swedish":
        # English → Swedish: always typing
        prompt = f"'{word['english']}' → "
        correct_answer = word["swedish"]
        answer = input(prompt).strip().lower()
        if answer == correct_answer.lower():
            print("✅ Correct!\n")
            s["correct"] += 1
            save_stats()
            return True
        else:
            print(f"❌ Correct answer: {correct_answer}\n")
            save_stats()
            return False

    else:
        # Swedish → English: always multiple choice
        prompt = f"'{word['swedish']}' → "
        correct_answer = word["english"]
        wrong_options = random.sample(
            [w["english"] for w in words if w != word],
            3
        )
        options = wrong_options + [correct_answer]
        random.shuffle(options)
        print(prompt)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")

        answer = input("Your answer (1-4): ").strip()
        try:
            if options[int(answer) - 1].lower() == correct_answer.lower():
                print("✅ Correct!\n")
                s["correct"] += 1
                save_stats()
                return True
            else:
                print(f"❌ Correct answer: {correct_answer}\n")
                save_stats()
                return False
        except (ValueError, IndexError):
            print(f"⚠️ Invalid input. Correct answer: {correct_answer}\n")
            save_stats()
            return False

# --- Main loop ---
print("=== 🇸🇪 Swedish Function Words Quiz ===")
print("Swedish → English: Multiple choice")
print("English → Swedish: Typing\n")
print("Ctrl+C to quit.\n")

score = 0
total = 0

try:
    while True:
        word = weighted_choice(words)
        total += 1
        if ask_question(word):
            score += 1
except KeyboardInterrupt:
    print("\n👋 Goodbye!")
    save_stats()