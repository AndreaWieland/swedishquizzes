import random

nouns = [
    {"swedish": "bil", "english": "car", "gender": "en", "plural": "bilar"},
    {"swedish": "bok", "english": "book", "gender": "en", "plural": "böcker"},
    {"swedish": "hund", "english": "dog", "gender": "en", "plural": "hundar"},
    {"swedish": "katt", "english": "cat", "gender": "en", "plural": "katter"},
    {"swedish": "hus", "english": "house", "gender": "ett", "plural": "hus"},
    {"swedish": "barn", "english": "child", "gender": "ett", "plural": "barn"},
    {"swedish": "bord", "english": "table", "gender": "ett", "plural": "bord"},
    {"swedish": "stol", "english": "chair", "gender": "en", "plural": "stolar"},
    {"swedish": "fönster", "english": "window", "gender": "ett", "plural": "fönster"},
    {"swedish": "dator", "english": "computer", "gender": "en", "plural": "datorer"},
    {"swedish": "telefon", "english": "phone", "gender": "en", "plural": "telefoner"},
    {"swedish": "vän", "english": "friend", "gender": "en", "plural": "vänner"},
    {"swedish": "jobb", "english": "job", "gender": "ett", "plural": "jobb"},
    {"swedish": "stad", "english": "city", "gender": "en", "plural": "städer"},
    {"swedish": "land", "english": "country", "gender": "ett", "plural": "länder"},
    {"swedish": "skola", "english": "school", "gender": "en", "plural": "skolor"},
    {"swedish": "lärare", "english": "teacher", "gender": "en", "plural": "lärare"},
    {"swedish": "elev", "english": "student/pupil", "gender": "en", "plural": "elever"},
    {"swedish": "mat", "english": "food", "gender": "en", "plural": "rätter"},
    {"swedish": "middag", "english": "dinner", "gender": "en", "plural": "middagar"},
    {"swedish": "frukost", "english": "breakfast", "gender": "en", "plural": "frukostar"},
    {"swedish": "kaffe", "english": "coffee", "gender": "ett", "plural": "kaffen"},
    {"swedish": "te", "english": "tea", "gender": "ett", "plural": "teer"},
    {"swedish": "vatten", "english": "water", "gender": "ett", "plural": "vatten"},
    {"swedish": "öl", "english": "beer", "gender": "en", "plural": "öl"},
    {"swedish": "vin", "english": "wine", "gender": "ett", "plural": "viner"},
    {"swedish": "dag", "english": "day", "gender": "en", "plural": "dagar"},
    {"swedish": "natt", "english": "night", "gender": "en", "plural": "nätter"},
    {"swedish": "vecka", "english": "week", "gender": "en", "plural": "veckor"},
    {"swedish": "månad", "english": "month", "gender": "en", "plural": "månader"},
    {"swedish": "år", "english": "year", "gender": "ett", "plural": "år"},
    {"swedish": "tid", "english": "time", "gender": "en", "plural": "tider"},
    {"swedish": "peng", "english": "coin", "gender": "en", "plural": "pengar"},
    {"swedish": "butik", "english": "shop", "gender": "en", "plural": "butiker"},
    {"swedish": "affär", "english": "store", "gender": "en", "plural": "affärer"},
    {"swedish": "pris", "english": "price", "gender": "ett", "plural": "priser"},
    {"swedish": "arbete", "english": "work", "gender": "ett", "plural": "arbeten"},
    {"swedish": "plats", "english": "place", "gender": "en", "plural": "platser"},
    {"swedish": "rum", "english": "room", "gender": "ett", "plural": "rum"},
    {"swedish": "väg", "english": "road", "gender": "en", "plural": "vägar"},
    {"swedish": "gata", "english": "street", "gender": "en", "plural": "gator"},
    {"swedish": "dörr", "english": "door", "gender": "en", "plural": "dörrar"},
    {"swedish": "nyckel", "english": "key", "gender": "en", "plural": "nycklar"},
    {"swedish": "biljett", "english": "ticket", "gender": "en", "plural": "biljetter"},
    {"swedish": "buss", "english": "bus", "gender": "en", "plural": "bussar"},
    {"swedish": "tåg", "english": "train", "gender": "ett", "plural": "tåg"},
    {"swedish": "flygplan", "english": "airplane", "gender": "ett", "plural": "flygplan"},
    {"swedish": "resa", "english": "trip", "gender": "en", "plural": "resor"},
    {"swedish": "semester", "english": "vacation", "gender": "en", "plural": "semestrar"},
    {"swedish": "hav", "english": "sea", "gender": "ett", "plural": "hav"},
    {"swedish": "sjö", "english": "lake", "gender": "en", "plural": "sjöar"},
    {"swedish": "berg", "english": "mountain", "gender": "ett", "plural": "berg"},
    {"swedish": "flod", "english": "river", "gender": "en", "plural": "floder"},
    {"swedish": "skog", "english": "forest", "gender": "en", "plural": "skogar"},
    {"swedish": "blomma", "english": "flower", "gender": "en", "plural": "blommor"},
    {"swedish": "träd", "english": "tree", "gender": "ett", "plural": "träd"},
    {"swedish": "växt", "english": "plant", "gender": "en", "plural": "växter"},
    {"swedish": "väder", "english": "weather", "gender": "ett", "plural": "väder"},
    {"swedish": "sol", "english": "sun", "gender": "en", "plural": "solar"},
    {"swedish": "måne", "english": "moon", "gender": "en", "plural": "månar"},
    {"swedish": "stjärna", "english": "star", "gender": "en", "plural": "stjärnor"},
    {"swedish": "familj", "english": "family", "gender": "en", "plural": "familjer"},
    {"swedish": "mamma", "english": "mother", "gender": "en", "plural": "mammor"},
    {"swedish": "pappa", "english": "father", "gender": "en", "plural": "pappor"},
    {"swedish": "syster", "english": "sister", "gender": "en", "plural": "systrar"},
    {"swedish": "bror", "english": "brother", "gender": "en", "plural": "bröder"},
    {"swedish": "barnbarn", "english": "grandchild", "gender": "ett", "plural": "barnbarn"},
    {"swedish": "människa", "english": "person/human", "gender": "en", "plural": "människor"},
    {"swedish": "man", "english": "man", "gender": "en", "plural": "män"},
    {"swedish": "kvinna", "english": "woman", "gender": "en", "plural": "kvinnor"},
    {"swedish": "pojke", "english": "boy", "gender": "en", "plural": "pojkar"},
    {"swedish": "flicka", "english": "girl", "gender": "en", "plural": "flickor"},
    {"swedish": "kropp", "english": "body", "gender": "en", "plural": "kroppar"},
    {"swedish": "hand", "english": "hand", "gender": "en", "plural": "händer"},
    {"swedish": "fot", "english": "foot", "gender": "en", "plural": "fötter"},
    {"swedish": "huvud", "english": "head", "gender": "ett", "plural": "huvuden"},
    {"swedish": "ansikte", "english": "face", "gender": "ett", "plural": "ansikten"},
    {"swedish": "öga", "english": "eye", "gender": "ett", "plural": "ögon"},
    {"swedish": "öra", "english": "ear", "gender": "ett", "plural": "öron"},
    {"swedish": "mun", "english": "mouth", "gender": "en", "plural": "munnar"},
    {"swedish": "näs", "english": "nose", "gender": "en", "plural": "näsor"},
    {"swedish": "hjärta", "english": "heart", "gender": "ett", "plural": "hjärtan"},
    {"swedish": "sjukdom", "english": "illness", "gender": "en", "plural": "sjukdomar"},
    {"swedish": "läkare", "english": "doctor", "gender": "en", "plural": "läkare"},
    {"swedish": "sjukhus", "english": "hospital", "gender": "ett", "plural": "sjukhus"},
    {"swedish": "pengar", "english": "money", "gender": "–", "plural": "pengar"},
    {"swedish": "brev", "english": "letter", "gender": "ett", "plural": "brev"},
    {"swedish": "tidning", "english": "newspaper", "gender": "en", "plural": "tidningar"},
    {"swedish": "bokhandel", "english": "bookstore", "gender": "en", "plural": "bokhandlar"},
    {"swedish": "film", "english": "movie", "gender": "en", "plural": "filmer"},
    {"swedish": "musik", "english": "music", "gender": "en", "plural": "musiker"},
    {"swedish": "sång", "english": "song", "gender": "en", "plural": "sånger"},
    {"swedish": "språk", "english": "language", "gender": "ett", "plural": "språk"},
    {"swedish": "landskap", "english": "landscape", "gender": "ett", "plural": "landskap"},
    {"swedish": "färg", "english": "color", "gender": "en", "plural": "färger"},
    {"swedish": "ljus", "english": "light", "gender": "ett", "plural": "ljus"},
    {"swedish": "skugga", "english": "shadow", "gender": "en", "plural": "skuggor"},
    {"swedish": "vänskap", "english": "friendship", "gender": "en", "plural": "vänskaper"},
    {"swedish": "dröm", "english": "dream", "gender": "en", "plural": "drömmar"},
    {"swedish": "historia", "english": "story/history", "gender": "en", "plural": "historier"},
    {"swedish": "problem", "english": "problem", "gender": "ett", "plural": "problem"},
    {"swedish": "fråga", "english": "question", "gender": "en", "plural": "frågor"},
    {"swedish": "svar", "english": "answer", "gender": "ett", "plural": "svar"},
    {"swedish": "idé", "english": "idea", "gender": "en", "plural": "idéer"},
    {"swedish": "liv", "english": "life", "gender": "ett", "plural": "liv"},
]

print("=== 🇸🇪 Swedish Nouns Quiz (B1 Level) ===")
print("Type your answer and press Enter. Ctrl+C to quit.\n")

score = 0
total = 0

try:
    while True:
        word = random.choice(nouns)
        total += 1

        question_type = random.choice(["article", "plural", "translation"])
        if question_type == "article":
            answer = input(f"What is the correct article for '{word['swedish']}'? (en/ett): ").strip().lower()
            correct = word["gender"]
        elif question_type == "plural":
            answer = input(f"What is the plural of '{word['swedish']}'? ").strip().lower()
            correct = word["plural"]
        else:  # translation
            direction = random.choice(["to_english", "to_swedish"])
            if direction == "to_english":
                answer = input(f"What is the English meaning of '{word['swedish']}'? ").strip().lower()
                correct = word["english"]
            else:
                answer = input(f"What is the Swedish word for '{word['english']}'? ").strip().lower()
                correct = word["swedish"]

        if answer == correct.lower():
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. The correct answer is: '{correct}'\n")

        print(f"Score: {score}/{total} ({round(score/total*100,1)}%)\n")

except KeyboardInterrupt:
    print(f"\n👋 Goodbye! You scored {score}/{total} ({round(score/total*100,1)}%)")
    print("Lycka till med din svenska!")
