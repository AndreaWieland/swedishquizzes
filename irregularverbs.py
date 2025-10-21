import json
import random
verbs = [
    {"english": "be", "infinitive": "vara", "present": "är", "past": "var", "supine": "varit", "imperative": "var"},
    {"english": "become", "infinitive": "bli", "present": "blir", "past": "blev", "supine": "blivit", "imperative": "bli"},
    {"english": "do/make", "infinitive": "göra", "present": "gör", "past": "gjorde", "supine": "gjort", "imperative": "gör"},
    {"english": "go", "infinitive": "gå", "present": "går", "past": "gick", "supine": "gått", "imperative": "gå"},
    {"english": "come", "infinitive": "komma", "present": "kommer", "past": "kom", "supine": "kommit", "imperative": "kom"},
    {"english": "get/receive", "infinitive": "få", "present": "får", "past": "fick", "supine": "fått", "imperative": "få"},
    {"english": "give", "infinitive": "ge", "present": "ger", "past": "gav", "supine": "gett", "imperative": "ge"},
    {"english": "see", "infinitive": "se", "present": "ser", "past": "såg", "supine": "sett", "imperative": "se"},
    # {"english": "sit", "infinitive": "sitta", "present": "sitter", "past": "satt", "supine": "suttit", "imperative": "sitt"},
    # {"english": "stand", "infinitive": "stå", "present": "står", "past": "stod", "supine": "stått", "imperative": "stå"},
    # {"english": "take", "infinitive": "ta", "present": "tar", "past": "tog", "supine": "tagit", "imperative": "ta"},
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
]

print("irregular verbs")
print("Type your answer and press Enter. Ctrl+C to quit.\n")
try:
    while True:
        verb = random.choice(verbs)
        
        # randomly ask from Swedish or English perspective
        direction = random.choice(["swedish", "english"])
        if direction == "swedish":
            tenses = ["present", "past", "supine", "imperative"]
            tense = random.choice(tenses)
            prompt = f"{tense} form of '{verb['infinitive']}' (in English: {verb['english']})? "
            correct = verb[tense]
        else:
            tenses = ["infinitive","present", "past", "supine", "imperative"]
            tense = random.choice(tenses)
            prompt = f"{tense} form of '{verb['english']}'? "
            correct = verb[tense]
        answer = input(prompt).strip().lower()
        if answer == correct.lower():
            print("✅ Correct\n")
        else:
            print(f"❌ Incorrect. The correct answer is: '{correct}'\n")
except KeyboardInterrupt:
    print("\n👋 Goodbye! Lycka till med din svenska!")