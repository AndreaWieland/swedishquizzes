import json
import random
import os

STATS_FILE = "idiom_preposition_stats.json"

# --- Idiomatic verb/adjective + preposition pairs ---
phrases = [
    {"base": "intresserad", "prep": "av"},
    {"base": "rädd", "prep": "för"},
    {"base": "trött", "prep": "på"},
    {"base": "stolt", "prep": "över"},
    {"base": "arg", "prep": "på"},
    {"base": "glad", "prep": "över"},
    {"base": "orolig", "prep": "för"},
    {"base": "nöjd", "prep": "med"},
    {"base": "van", "prep": "vid"},
    {"base": "beroende", "prep": "av"},
    {"base": "tacka", "prep": "för"},
    {"base": "vänta", "prep": "på"},
    {"base": "tala", "prep": "om"},
    {"base": "drömma", "prep": "om"},
    {"base": "oroa sig", "prep": "för"},
    {"base": "bry sig", "prep": "om"},
    {"base": "skriva", "prep": "till"},
    {"base": "lyssna", "prep": "på"},
    {"base": "titta", "prep": "på"},
    {"base": "lita", "prep": "på"},
    {"base": "be", "prep": "om"},
    {"base": "tänka", "prep": "på"},
    {"base": "tycka", "prep": "om"},
    {"base": "delta", "prep": "i"},
    {"base": "hjälpa", "prep": "till"},
    {"base": "ansvara", "prep": "för"},
    {"base": "bestämma sig", "prep": "för"},
    {"base": "förlita sig", "prep": "på"},
    {"base": "skratta", "prep": "åt"},
    {"base": "satsa", "prep": "på"},
    {"base": "hålla med", "prep": ""},
    {"base": "hålla på", "prep": "med"},
    {"base": "leka", "prep": "med"},
    {"base": "diskutera", "prep": "om"},
    {"base": "berätta", "prep": "om"},
    {"base": "förklara", "prep": "för"},
    {"base": "tacka", "prep": "för"},
    {"base": "längta", "prep": "efter"},
    {"base": "vänja sig", "prep": "vid"},
    {"base": "kämpa", "prep": "för"},
    {"base": "oroa", "prep": "över"},
    {"base": "läsa", "prep": "om"},
    {"base": "driva", "prep": "med"},
    {"base": "bråka", "prep": "med"},
    {"base": "argumentera", "prep": "för"},
    {"base": "påminna", "prep": "om"},
    {"base": "koncentrera sig", "prep": "på"},
    {"base": "respektera", "prep": ""},
    {"base": "förlora", "prep": "mot"},
    {"base": "vinna", "prep": "över"},
    {"base": "handla", "prep": "om"},
    {"base": "bjuda", "prep": "in"},
]

# --- Stats handling ---
if os.path.exists(STATS_FILE):
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)
else:
    stats = {}

for p in phrases:
    base = p["base"]
    if base not in stats:
        stats[base] = {"asked": 0, "correct": 0}

LEVEL_UP_THRESHOLD = 0.8
MIN_ASKS_FOR_LEVELUP = 5

def save_stats():
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def weighted_choice(items):
    weights = []
    for p in items:
        s = stats[p["base"]]
        asked, correct = s["asked"], s["correct"]
        if asked == 0:
            weight = 4.0
        else:
            acc = correct / asked
            weight = max(0.5, 4.0 * (1 - acc))
        weights.append(weight)
    return random.choices(items, weights=weights, k=1)[0]

def ask_question(entry):
    s = stats[entry["base"]]
    asked, correct = s["asked"], s["correct"]
    accuracy = correct / asked if asked > 0 else 0
    typing_mode = asked >= MIN_ASKS_FOR_LEVELUP and accuracy >= LEVEL_UP_THRESHOLD

    s["asked"] += 1
    correct_answer = entry["prep"]

    # --- Typing mode ---
    if typing_mode:
        ans = input(f"Vilken preposition passar med '{entry['base']}'? → ").strip().lower()
        if ans == correct_answer.lower():
            print("✅ Rätt!\n")
            s["correct"] += 1
        else:
            print(f"❌ Rätt svar: '{correct_answer}'\n")
        save_stats()
        return

    # --- Multiple choice mode ---
    wrong_opts = random.sample(
        [p["prep"] for p in phrases if p["prep"] != correct_answer and p["prep"] != ""],
        3
    )
    options = wrong_opts + [correct_answer]
    random.shuffle(options)

    print(f"Vilken preposition passar med '{entry['base']}'?")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")

    ans = input("Ditt svar (1-4): ").strip()
    try:
        if options[int(ans) - 1].lower() == correct_answer.lower():
            print("✅ Rätt!\n")
            s["correct"] += 1
        else:
            print(f"❌ Rätt svar: '{correct_answer}'\n")
    except (ValueError, IndexError):
        print(f"⚠️ Ogiltigt svar. Rätt svar: '{correct_answer}'\n")

    save_stats()

# --- Main loop ---
print("=== 🇸🇪 Svenska Verb + Prepositioner Quiz ===")
print("Flera val → Skriva när du har lärt dig.\n")

try:
    while True:
        ask_question(weighted_choice(phrases))
except KeyboardInterrupt:
    print("\n👋 Hej då!")
    save_stats()
