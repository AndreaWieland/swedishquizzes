import random

# Focused list of very common Swedish connection words and phrases
connectors = [
    {"english": "and", "swedish": "och"},
    {"english": "but", "swedish": "men"},
    {"english": "or", "swedish": "eller"},
    {"english": "because", "swedish": "eftersom"},
    {"english": "so that", "swedish": "så att"},
    {"english": "if", "swedish": "om"},
    {"english": "when", "swedish": "när"},
    {"english": "while", "swedish": "medan"},
    {"english": "before", "swedish": "innan"},
    {"english": "after", "swedish": "efter att"},
    {"english": "although", "swedish": "fastän"},
    {"english": "even though", "swedish": "även om"},
    {"english": "therefore", "swedish": "därför"},
    {"english": "so / then", "swedish": "så"},
    {"english": "however", "swedish": "dock"},
    {"english": "for example", "swedish": "till exempel"},
    {"english": "in addition", "swedish": "dessutom"},
    {"english": "on the other hand", "swedish": "å andra sidan"},
    {"english": "that is / i.e.", "swedish": "det vill säga"},
    {"english": "instead", "swedish": "istället"},
    {"english": "because of", "swedish": "på grund av"},
    {"english": "despite", "swedish": "trots"},
    {"english": "as soon as", "swedish": "så snart som"},
    {"english": "until", "swedish": "tills"},
    {"english": "since", "swedish": "sedan"},
    {"english": "therefore / that’s why", "swedish": "därför att"},
]

def ask_multiple_choice(question, correct_answer, options):
    random.shuffle(options)
    print(question)
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    choice = input("Your answer (1-4): ").strip()
    try:
        if options[int(choice)-1].lower() == correct_answer.lower():
            print("✅ Correct!\n")
            return True
        else:
            print(f"❌ Incorrect. Correct answer: {correct_answer}\n")
            return False
    except (ValueError, IndexError):
        print(f"⚠️ Invalid input. Correct answer was: {correct_answer}\n")
        return False


print("=== 🇸🇪 Swedish Connection Words Quiz (B1 Level) ===")
print("Type the number of your answer. Ctrl+C to quit.\n")

score = 0
total = 0

try:
    while True:
        total += 1
        word = random.choice(connectors)
        direction = random.choice(["to_swedish", "to_english"])

        # Build wrong options
        wrong_options = random.sample(
            [w["swedish"] if direction == "to_swedish" else w["english"]
             for w in connectors if w != word],
            3
        )

        if direction == "to_swedish":
            question = f"What is the Swedish word for '{word['english']}'?"
            correct = word["swedish"]
            options = wrong_options + [correct]
        else:
            question = f"What is the English meaning of '{word['swedish']}'?"
            correct = word["english"]
            options = wrong_options + [correct]

        if ask_multiple_choice(question, correct, options):
            score += 1

        print(f"Score: {score}/{total} ({round(score/total*100,1)}%)\n")

except KeyboardInterrupt:
    print("\n👋 Goodbye! You scored", f"{score}/{total} ({round(score/total*100,1)}%)")
    print("Lycka till med din svenska!")
