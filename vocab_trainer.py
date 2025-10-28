import json
import random
import os
import importlib

# ===============================
#  MENU AND IMPORT
# ===============================

TOPICS = {
    "1": "society",
    "2": "irregular_verbs",
    "3": "connection_words",
    "4": "health_and_wellness",
    "5": "family",
    "6": "pronouns"
}

print("=== 🇸🇪 Swedish Vocabulary Trainer ===")
print("Select a topic:\n")

for key, topic in TOPICS.items():
    print(f"{key}. {topic.replace('_', ' ').title()}")

choice = input("\nEnter number: ").strip()
if choice not in TOPICS:
    print("Invalid choice. Exiting.")
    exit(0)

topic_name = TOPICS[choice]
STATS_FILE = f"{topic_name}_stats.json"

try:
    topic_module = importlib.import_module(f"topics.{topic_name}")
except ModuleNotFoundError:
    print(f"❌ Could not find file '{topic_name}.py'.")
    exit(1)

all_nouns = getattr(topic_module, "nouns", [])
all_verbs = getattr(topic_module, "verbs", [])

if not all_nouns and not all_verbs:
    print(f"⚠️ Warning: '{topic_name}' has no nouns or verbs defined.")
    exit(0)

print(f"\n📚 Loaded topic: {topic_name.replace('_', ' ').title()}")
print(f"   Nouns: {len(all_nouns)} | Verbs: {len(all_verbs)}")
print("   Ctrl+C to quit.\n")

# ===============================
#  STATS HANDLING
# ===============================

if os.path.exists(STATS_FILE):
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)
else:
    stats = {}

def ensure_stats(entry, tense=None):
    if entry["type"] == "noun":
        key = f"noun-{entry['swedish']}"
    else:
        key = f"verb-{entry['infinitive']}-{tense or 'infinitive'}"
    if key not in stats:
        stats[key] = {"asked": 0, "correct": 0}

def save_stats():
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

# ===============================
#  ADAPTIVE WEIGHTING
# ===============================

def get_accuracy(rec):
    a, c = rec["asked"], rec["correct"]
    return c / a if a > 0 else 0.0

def get_weight(entry, tense=None):
    if entry["type"] == "noun":
        key = f"noun-{entry['swedish']}"
    else:
        key = f"verb-{entry['infinitive']}-{tense}"
    rec = stats.get(key, {"asked": 0, "correct": 0})
    if rec["asked"] == 0:
        return 4.0
    acc = get_accuracy(rec)
    return max(0.5, 4.0 * (1 - acc))

# ===============================
#  PROGRESSIVE UNLOCK SYSTEM
# ===============================

START_SIZE = 5
UNLOCK_BATCH = 5
MASTERY_THRESHOLD = 0.5
MIN_ATTEMPTS = 2

active_nouns = all_nouns[:START_SIZE]
active_verbs = all_verbs[:START_SIZE]

def is_mastered(entry, tense=None):
    if entry["type"] == "noun":
        key = f"noun-{entry['swedish']}"
        rec = stats.get(key, {"asked": 0, "correct": 0})
        if rec["asked"] < MIN_ATTEMPTS:
            return False
        acc = get_accuracy(rec)
        return acc >= MASTERY_THRESHOLD

    total_asked = total_correct = 0
    for t in ["infinitive", "present", "past", "supine", "imperative"]:
        key = f"verb-{entry['infinitive']}-{t}"
        rec = stats.get(key, {"asked": 0, "correct": 0})
        total_asked += rec["asked"]
        total_correct += rec["correct"]

    if total_asked < MIN_ATTEMPTS * 2:
        return False

    acc = total_correct / total_asked if total_asked else 0
    return acc >= MASTERY_THRESHOLD

def update_active_words():
    global active_nouns, active_verbs

    if active_nouns:
        mastered_nouns = sum(is_mastered(n) for n in active_nouns)
        if mastered_nouns == len(active_nouns) and len(active_nouns) < len(all_nouns):
            next_n = min(len(all_nouns), len(active_nouns) + UNLOCK_BATCH)
            print(f"🌱 Added {next_n - len(active_nouns)} new nouns! Total active: {next_n}")
            active_nouns = all_nouns[:next_n]

    if active_verbs:
        mastered_verbs = sum(is_mastered(v) for v in active_verbs)
        if mastered_verbs == len(active_verbs) and len(active_verbs) < len(all_verbs):
            next_v = min(len(all_verbs), len(active_verbs) + UNLOCK_BATCH)
            print(f"🌱 Added {next_v - len(active_verbs)} new verbs! Total active: {next_v}")
            active_verbs = all_verbs[:next_v]

# ===============================
#  QUESTION FUNCTIONS
# ===============================

def ask_noun(noun):
    key = f"noun-{noun['swedish']}"
    ensure_stats(noun)
    stats[key]["asked"] += 1
    direction = random.choice(["to_english", "to_swedish"])

    if direction == "to_swedish":
        answer = input(f"'{noun['english']}' → ").strip().lower()
        if answer == noun["swedish"].lower():
            print("✅ Correct!\n")
            stats[key]["correct"] += 1
        else:
            print(f"❌ Correct answer: {noun['swedish']}\n")
    else:
        prompt = f"'{noun['swedish']}' → "
        correct = noun["english"]
        wrong = random.sample([n["english"] for n in active_nouns if n != noun], k=min(3, len(active_nouns)-1))
        options = wrong + [correct]
        random.shuffle(options)
        print(prompt)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        choice = input("Your answer (1-4): ").strip()
        try:
            if options[int(choice) - 1].lower() == correct.lower():
                print("✅ Correct!\n")
                stats[key]["correct"] += 1
            else:
                print(f"❌ Correct answer: {correct}\n")
        except:
            print(f"⚠️ Invalid input. Correct answer: {correct}\n")

    save_stats()
    update_active_words()

def ask_verb(verb):
    tense = random.choice(["infinitive", "present", "past", "supine", "imperative"])
    key = f"verb-{verb['infinitive']}-{tense}"
    ensure_stats(verb, tense)
    stats[key]["asked"] += 1

    direction = random.choice(["swedish", "english"])
    correct = verb[tense]

    if direction == "swedish":
        prompt = f"{tense} form of '{verb['infinitive']}' (English: {verb['english']})? "
    else:
        prompt = f"{tense} form of '{verb['english']}'? "

    answer = input(prompt).strip().lower()
    if answer == correct.lower():
        print("✅ Correct!\n")
        stats[key]["correct"] += 1
    else:
        print(f"❌ Correct answer: {correct}\n")

    save_stats()
    update_active_words()

# ===============================
#  MAIN LOOP
# ===============================

try:
    while True:
        available_types = []
        if active_nouns:
            available_types.append("noun")
        if active_verbs:
            available_types.append("verb")

        if not available_types:
            print("🎉 You've mastered everything in this topic!")
            break

        choice_type = random.choice(available_types)

        if choice_type == "noun":
            weights = [get_weight(n) for n in active_nouns]
            noun = random.choices(active_nouns, weights=weights, k=1)[0]
            ask_noun(noun)
        else:
            weighted = []
            for v in active_verbs:
                for tense in ["infinitive", "present", "past", "supine", "imperative"]:
                    weighted.append((v, tense, get_weight(v, tense)))
            (verb, tense, _) = random.choices(weighted, weights=[w for _, _, w in weighted], k=1)[0]
            ask_verb(verb)

except KeyboardInterrupt:
    print("\n👋 Goodbye! Lycka till med din svenska!")
    save_stats()
