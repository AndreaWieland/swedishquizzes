import json
import random
import os
import importlib

# ===============================
#  MENU AND IMPORT
# ===============================

TOPICS_DIR = "topics"

# Dynamically list available topic files
topic_files = [
    f[:-3] for f in os.listdir(TOPICS_DIR)
    if f.endswith(".py") and f != "__init__.py"
]

if not topic_files:
    print("❌ No topic files found in 'topics/' directory.")
    exit(1)

# Build topic dictionary dynamically with numbered keys
TOPICS = {str(i + 1): name for i, name in enumerate(sorted(topic_files))}

print("=== 🇸🇪 Swedish Vocabulary Trainer ===")
print("Select a topic:\n")

for key, topic in TOPICS.items():
    print(f"{key}. {topic.replace('_', ' ').title()}")

choice = input("\nEnter number: ").strip()
if choice not in TOPICS:
    print("Invalid choice. Exiting.")
    exit(0)

topic_name = TOPICS[choice]
STATS_FILE = f"stats/{topic_name}_stats.json"

try:
    topic_module = importlib.import_module(f"topics.{topic_name}")
except ModuleNotFoundError:
    print(f"❌ Could not find file '{topic_name}.py'.")
    exit(1)

all_nouns = getattr(topic_module, "nouns", [])
all_verbs = getattr(topic_module, "verbs", [])
all_misc = getattr(topic_module, "misc", [])

if not all_nouns and not all_verbs and not all_misc:
    print(f"⚠️ Warning: '{topic_name}' has no vocabulary defined.")
    exit(0)

print(f"\n📚 Loaded topic: {topic_name.replace('_', ' ').title()}")
print(f"   Nouns: {len(all_nouns)} | Verbs: {len(all_verbs)} | Misc: {len(all_misc)}")
print("   Ctrl+C to quit.\n")

# ===============================
#  STATS HANDLING
# ===============================

if os.path.exists(STATS_FILE):
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)
else:
    stats = {}

def ensure_stats(category, key):
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

def get_weight(category, key):
    rec = stats.get(key, {"asked": 0, "correct": 0})
    if rec["asked"] == 0:
        return 4.0
    return max(0.5, 4.0 * (1 - get_accuracy(rec)))

# ===============================
#  PROGRESSIVE UNLOCK SYSTEM
# ===============================

START_SIZE = 5
UNLOCK_BATCH = 7
MASTERY_THRESHOLD = 0.8
MIN_ATTEMPTS = 2

active_nouns = all_nouns[:START_SIZE]
active_verbs = all_verbs[:START_SIZE]
active_misc = all_misc[:START_SIZE]

def is_mastered(entry, category=None, tense=None):
    if category == "misc":
        key = f"misc-{entry['swedish']}"
        rec = stats.get(key, {"asked": 0, "correct": 0})
        if rec["asked"] < MIN_ATTEMPTS:
            return False
        return get_accuracy(rec) >= MASTERY_THRESHOLD

    if "indefinite" in entry:
        # Noun
        key = f"noun-{entry['indefinite']}"
        rec = stats.get(key, {"asked": 0, "correct": 0})
        if rec["asked"] < MIN_ATTEMPTS:
            return False
        return get_accuracy(rec) >= MASTERY_THRESHOLD

    if "infinitive" in entry:
        # Verb
        total_asked = total_correct = 0
        for t in ["infinitive", "present", "past", "supine", "imperative"]:
            key = f"verb-{entry['infinitive']}-{t}"
            rec = stats.get(key, {"asked": 0, "correct": 0})
            total_asked += rec["asked"]
            total_correct += rec["correct"]
        if total_asked < MIN_ATTEMPTS * 2:
            return False
        return (total_correct / total_asked) >= MASTERY_THRESHOLD

    return False

def update_active_words():
    global active_nouns, active_verbs, active_misc

    # Nouns
    if active_nouns:
        mastered_nouns = sum(is_mastered(n) for n in active_nouns)
        if mastered_nouns / len(active_nouns) >= 0.7 and len(active_nouns) < len(all_nouns):
            next_n = min(len(all_nouns), len(active_nouns) + UNLOCK_BATCH)
            print(f"🌱 Added {next_n - len(active_nouns)} new nouns! Total active: {next_n}")
            active_nouns = all_nouns[:next_n]

    # Verbs
    if active_verbs:
        mastered_verbs = sum(is_mastered(n) for n in active_verbs)
        if mastered_verbs / len(active_verbs) >= 0.7 and len(active_verbs) < len(all_verbs):
            next_v = min(len(all_verbs), len(active_verbs) + UNLOCK_BATCH)
            print(f"🌱 Added {next_v - len(active_verbs)} new verbs! Total active: {next_v}")
            active_verbs = all_verbs[:next_v]

    # Misc
    if active_misc:
        mastered_misc = sum(is_mastered(n, "misc") for n in active_misc)
        if mastered_misc / len(active_misc) >= 0.7 and len(active_misc) < len(all_misc):
            next_m = min(len(all_misc), len(active_misc) + UNLOCK_BATCH)
            print(f"🌱 Added {next_m - len(active_misc)} new misc words! Total active: {next_m}")
            active_misc = all_misc[:next_m]

# ===============================
#  QUESTION FUNCTIONS
# ===============================

def ask_noun(noun):
    # Randomly pick a form to quiz
    forms = ["indefinite", "definite", "plural", "plural_definite"]
    form = random.choice(forms)
    key = f"noun-{noun['indefinite']}-{form}"
    ensure_stats("noun", key)
    stats[key]["asked"] += 1

    direction = random.choice(["to_english", "to_swedish"])

    if direction == "to_english":
        # Swedish form shown, ask for English
        swedish_word = noun.get(form, noun["indefinite"])
        correct = noun["english"]
        # multiple choice options
        wrong = random.sample(
            [n["english"] for n in active_nouns if n != noun],
            k=min(3, len(active_nouns)-1)
        ) if len(active_nouns) > 1 else []
        options = wrong + [correct]
        random.shuffle(options)

        print(f"What is the English meaning of '{swedish_word}'?")
        for i,opt in enumerate(options,1):
            print(f"  {i}. {opt}")
        choice = input("Your answer (1-4): ").strip()
        try:
            if options[int(choice)-1].lower() == correct.lower():
                print("✅ Correct!\n")
                stats[key]["correct"] += 1
            else:
                print(f"❌ Correct answer: {correct}\n")
        except:
            print(f"⚠️ Invalid input. Correct answer: {correct}\n")

    else:
        # English shown, ask for Swedish form
        swedish_word = noun.get(form, noun["indefinite"])
        answer = input(f"What is the {form.replace('_',' ')} form of '{noun['english']}'? ").strip().lower()
        if answer == swedish_word.lower():
            print("✅ Correct!\n")
            stats[key]["correct"] += 1
        else:
            print(f"❌ Correct answer: {swedish_word}\n")

    save_stats()
    update_active_words()

def ask_verb(verb):
    # Random tense, avoid infinitive if showing Swedish
    tenses = ["infinitive", "present", "past", "supine", "imperative"]
    tense = random.choice(tenses)
    key = f"verb-{verb['infinitive']}-{tense}"
    ensure_stats("verb", key)
    stats[key]["asked"] += 1

    direction = random.choice(["swedish", "english"])
    correct = verb[tense]

    if direction == "swedish":
        if tense == "infinitive":
            # skip infinitive form quiz in Swedish
            return
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

def ask_misc(entry):
    key = f"misc-{entry['swedish']}"
    ensure_stats("misc", key)
    stats[key]["asked"] += 1

    direction = random.choices(
        ["to_english", "to_swedish"],
        weights=[0.2, 0.8],
        k=1
    )[0]

    if direction == "to_english":
        correct = entry["english"]
        wrong = random.sample(
            [m["english"] for m in active_misc if m != entry],
            k=min(3, len(active_misc)-1)
        ) if len(active_misc) > 1 else []
        options = wrong + [correct]
        random.shuffle(options)
        print(f"'{entry['swedish']}' →")
        for i,opt in enumerate(options,1):
            print(f"  {i}. {opt}")
        choice = input("Your answer (1-4): ").strip()
        try:
            if options[int(choice)-1].lower() == correct.lower():
                print("✅ Correct!\n")
                stats[key]["correct"] += 1
            else:
                print(f"❌ Correct answer: {correct}\n")
        except:
            print(f"⚠️ Invalid input. Correct answer: {correct}\n")
    else:
        answer = input(f"'{entry['english']}' → ").strip().lower()
        if answer == entry["swedish"].lower():
            print("✅ Correct!\n")
            stats[key]["correct"] += 1
        else:
            print(f"❌ Correct answer: {entry['swedish']}\n")

    save_stats()
    update_active_words()

# ===============================
#  MAIN LOOP
# ===============================

try:
    while True:
        available_types = []
        if active_nouns: available_types.append("noun")
        if active_verbs: available_types.append("verb")
        if active_misc: available_types.append("misc")

        if not available_types:
            print("🎉 You've mastered everything in this topic!")
            break

        choice_type = random.choice(available_types)

        if choice_type == "noun":
            weights = [get_weight("noun", f"noun-{n['indefinite']}") for n in active_nouns]
            noun = random.choices(active_nouns, weights=weights, k=1)[0]
            ask_noun(noun)
        elif choice_type == "verb":
            weighted = []
            for v in active_verbs:
                for t in ["infinitive","present","past","supine","imperative"]:
                    weighted.append((v,t,get_weight("verb", f"verb-{v['infinitive']}-{t}")))
            (verb,tense,_) = random.choices(weighted, weights=[w for _,_,w in weighted], k=1)[0]
            ask_verb(verb)
        else:  # misc
            weights = [get_weight("misc", f"misc-{m['swedish']}") for m in active_misc]
            misc = random.choices(active_misc, weights=weights, k=1)[0]
            ask_misc(misc)

except KeyboardInterrupt:
    print("\n👋 Goodbye! Lycka till med din svenska!")
    save_stats()
