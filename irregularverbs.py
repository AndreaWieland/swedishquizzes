import json
import random
import os

SAVE_FILE = "verb_stats.json"

verbs = [
    {"english": "be", "infinitive": "vara", "present": "är", "past": "var", "supine": "varit", "imperative": "var"},
    {"english": "become", "infinitive": "bli", "present": "blir", "past": "blev", "supine": "blivit", "imperative": "bli"},
    {"english": "do/make", "infinitive": "göra", "present": "gör", "past": "gjorde", "supine": "gjort", "imperative": "gör"},
    {"english": "go", "infinitive": "gå", "present": "går", "past": "gick", "supine": "gått", "imperative": "gå"},
    {"english": "come", "infinitive": "komma", "present": "kommer", "past": "kom", "supine": "kommit", "imperative": "kom"},
    {"english": "get/receive", "infinitive": "få", "present": "får", "past": "fick", "supine": "fått", "imperative": "få"},
    {"english": "give", "infinitive": "ge", "present": "ger", "past": "gav", "supine": "gett", "imperative": "ge"},
    {"english": "see", "infinitive": "se", "present": "ser", "past": "såg", "supine": "sett", "imperative": "se"},
    {"english": "sit", "infinitive": "sitta", "present": "sitter", "past": "satt", "supine": "suttit", "imperative": "sitt"},
    {"english": "stand", "infinitive": "stå", "present": "står", "past": "stod", "supine": "stått", "imperative": "stå"},
    {"english": "take", "infinitive": "ta", "present": "tar", "past": "tog", "supine": "tagit", "imperative": "ta"},
    {"english": "manage to", "infinitive": "lyckas", "present": "lyckas", "past": "lyckades", "supine": "lyckats", "imperative": "lyckas"},
    {"english": "try", "infinitive": "försöka", "present": "försöker", "past": "försökte", "supine": "försökt", "imperative": "försök"},
    {"english": "seem", "infinitive": "tyckas", "present": "tycks", "past": "tycktes", "supine": "tyckts", "imperative": "tyck"},
    {"english": "breathe", "infinitive": "andas", "present": "andas", "past": "andades", "supine": "andats", "imperative": "andas"},
    {"english": "happen", "infinitive": "hända", "present": "händer", "past": "hände", "supine": "hänt", "imperative": "hända"},
    {"english": "belong", "infinitive": "tillhöra", "present": "tillhör", "past": "tillhörde", "supine": "tillhört", "imperative": "tillhör"},
    {"english": "believe", "infinitive": "tro", "present": "tror", "past": "trodde", "supine": "trott", "imperative": "tro"},
    {"english": "seem", "infinitive": "synas", "present": "syns", "past": "syntes", "supine": "synts", "imperative": "syns"},
    {"english": "belong", "infinitive": "tillhöra", "present": "tillhör", "past": "tillhörde", "supine": "tillhört", "imperative": "tillhör"},
    {"english": "succeed", "infinitive": "lyckas", "present": "lyckas", "past": "lyckades", "supine": "lyckats", "imperative": "lyckas"},
    # {"english": "know (a fact)", "infinitive": "veta", "present": "vet", "past": "visste", "supine": "vetat", "imperative": "veta"},
    # {"english": "know (be familiar with)", "infinitive": "känna", "present": "känner", "past": "kände", "supine": "känt", "imperative": "känn"},
    # {"english": "say", "infinitive": "säga", "present": "säger", "past": "sa", "supine": "sagt", "imperative": "säg"},
    # {"english": "write", "infinitive": "skriva", "present": "skriver", "past": "skrev", "supine": "skrivit", "imperative": "skriv"},
    # {"english": "eat", "infinitive": "äta", "present": "äter", "past": "åt", "supine": "ätit", "imperative": "ät"},
    # {"english": "drink", "infinitive": "dricka", "present": "dricker", "past": "drack", "supine": "druckit", "imperative": "drick"},
    # {"english": "sleep", "infinitive": "sova", "present": "sover", "past": "sov", "supine": "sovit", "imperative": "sov"},
    # {"english": "run", "infinitive": "springa", "present": "springer", "past": "sprang", "supine": "sprungit", "imperative": "spring"},
    # {"english": "understand", "infinitive": "förstå", "present": "förstår", "past": "förstod", "supine": "förstått", "imperative": "förstå"},
    # {"english": "buy", "infinitive": "köpa", "present": "köper", "past": "köpte", "supine": "köpt", "imperative": "köp"},
    # {"english": "sell", "infinitive": "sälja", "present": "säljer", "past": "sålde", "supine": "sålt", "imperative": "sälj"},
    # {"english": "read", "infinitive": "läsa", "present": "läser", "past": "läste", "supine": "läst", "imperative": "läs"},
    # {"english": "lie (be lying)", "infinitive": "ligga", "present": "ligger", "past": "låg", "supine": "legat", "imperative": "ligg"},
    # {"english": "put/lay", "infinitive": "lägga", "present": "lägger", "past": "la", "supine": "lagt", "imperative": "lägg"},
    # {"english": "hold", "infinitive": "hålla", "present": "håller", "past": "höll", "supine": "hållit", "imperative": "håll"},
    # {"english": "meet", "infinitive": "träffa", "present": "träffar", "past": "träffade", "supine": "träffat", "imperative": "träffa"},
    # {"english": "help", "infinitive": "hjälpa", "present": "hjälper", "past": "hjälpte", "supine": "hjälpt", "imperative": "hjälp"},
    # {"english": "choose", "infinitive": "välja", "present": "väljer", "past": "valde", "supine": "valt", "imperative": "välj"},
    # {"english": "be able to / can", "infinitive": "kunna", "present": "kan", "past": "kunde", "supine": "kunnat", "imperative": "–"},
    # {"english": "must / have to", "infinitive": "måste", "present": "måste", "past": "måste", "supine": "måst", "imperative": "–"},
    # {"english": "want", "infinitive": "vilja", "present": "vill", "past": "ville", "supine": "velat", "imperative": "–"},
    # {"english": "shall / will", "infinitive": "skola", "present": "ska", "past": "skulle", "supine": "skolat", "imperative": "–"},
    # {"english": "need", "infinitive": "behöva", "present": "behöver", "past": "behövde", "supine": "behövt", "imperative": "behöv"},
    # {"english": "die", "infinitive": "dö", "present": "dör", "past": "dog", "supine": "dött", "imperative": "dö"},
    # {"english": "live", "infinitive": "leva", "present": "lever", "past": "levde", "supine": "levt", "imperative": "lev"},
    # {"english": "bring", "infinitive": "ta med", "present": "tar med", "past": "tog med", "supine": "tagit med", "imperative": "ta med"},
    # {"english": "begin", "infinitive": "börja", "present": "börjar", "past": "började", "supine": "börjat", "imperative": "börja"},
    # {"english": "drive", "infinitive": "köra", "present": "kör", "past": "körde", "supine": "kört", "imperative": "kör"},
    # {"english": "send", "infinitive": "skicka", "present": "skickar", "past": "skickade", "supine": "skickat", "imperative": "skicka"},
    # {"english": "wait", "infinitive": "vänta", "present": "väntar", "past": "väntade", "supine": "väntat", "imperative": "vänta"},
    # {"english": "win", "infinitive": "vinna", "present": "vinner", "past": "vann", "supine": "vunnit", "imperative": "vinn"},
    # {"english": "lose", "infinitive": "förlora", "present": "förlorar", "past": "förlorade", "supine": "förlorat", "imperative": "förlora"},
    # {"english": "think", "infinitive": "tänka", "present": "tänker", "past": "tänkte", "supine": "tänkt", "imperative": "tänk"},
    # {"english": "believe", "infinitive": "tro", "present": "tror", "past": "trodde", "supine": "trott", "imperative": "tro"},
    # {"english": "feel", "infinitive": "må", "present": "mår", "past": "mådde", "supine": "mått", "imperative": "må"}
    {"english": "invite", "infinitive": "bjuda", "present": "bjuder", "past": "bjöd", "supine": "bjudit", "imperative": "bjud"},
]

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)
else:
    stats = {}

def ensure_stats(verb, tense):
    key = f"{verb['infinitive']}-{tense}"
    if key not in stats:
        stats[key] = {"correct": 0, "wrong": 0}

def save_stats():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def get_weight(verb, tense):
    """Return weight for a verb-tense pair (higher = more likely)."""
    key = f"{verb['infinitive']}-{tense}"
    record = stats.get(key, {"correct": 0, "wrong": 0})
    wrong, correct = record["wrong"], record["correct"]
    total = wrong + correct
    if total == 0:
        return 1.5  # slightly favor unseen forms
    accuracy = correct / total if total > 0 else 0
    return max(0.2, 2.5 * (1 - accuracy))  # lower accuracy → higher weight

def choose_weighted(verbs):
    weighted = []
    for v in verbs:
        for tense in ["infinitive", "present", "past", "supine", "imperative"]:
            weighted.append((v, tense, get_weight(v, tense)))
    # choose a random direction (Swedish or English)
    (v, tense, _) = random.choices(weighted, weights=[w for _, _, w in weighted], k=1)[0]
    return v, tense

print("🇸🇪 Irregular Verb Trainer — per tense adaptive mode")
print("Type your answer and press Enter. Ctrl+C to quit.\n")

try:
    while True:
        direction = random.choice(["swedish", "english"])
        verb, tense = choose_weighted(verbs)
        ensure_stats(verb, tense)
        key = f"{verb['infinitive']}-{tense}"

        if direction == "swedish":
            prompt = f"{tense} form of '{verb['infinitive']}' (English: {verb['english']})? "
            correct = verb[tense]
        else:
            prompt = f"{tense} form of '{verb['english']}'? "
            correct = verb[tense]

        answer = input(prompt).strip().lower()
        if answer == correct.lower():
            print("✅ Correct!\n")
            stats[key]["correct"] += 1
        else:
            print(f"❌ Incorrect. Correct answer: '{correct}'\n")
            stats[key]["wrong"] += 1

        save_stats()

except KeyboardInterrupt:
    print("\n👋 Goodbye! Lycka till med din svenska!")
    save_stats()