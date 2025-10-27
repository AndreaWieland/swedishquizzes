import json
import random
import os

STATS_FILE = "society_stats.json"

all_nouns = [
    {"type": "noun", "swedish": "samhället", "english": "society"},
    {"type": "noun", "swedish": "medborgare", "english": "citizen"},
    {"type": "noun", "swedish": "rättighet", "english": "right"},
    {"type": "noun", "swedish": "skyldighet", "english": "obligation"},
    {"type": "noun", "swedish": "regering", "english": "government"},
    {"type": "noun", "swedish": "riksdag", "english": "parliament"},
    {"type": "noun", "swedish": "lag", "english": "law"},
    {"type": "noun", "swedish": "regel", "english": "rule"},
    {"type": "noun", "swedish": "minister", "english": "minister"},
    {"type": "noun", "swedish": "politiker", "english": "politician"},
    {"type": "noun", "swedish": "parti", "english": "party (political)"},
    {"type": "noun", "swedish": "val", "english": "election"},
    {"type": "noun", "swedish": "omröstning", "english": "vote"},
    {"type": "noun", "swedish": "demokrati", "english": "democracy"},
    {"type": "noun", "swedish": "diktatur", "english": "dictatorship"},
    {"type": "noun", "swedish": "frihet", "english": "freedom"},
    {"type": "noun", "swedish": "jämlikhet", "english": "equality"},
    {"type": "noun", "swedish": "rättvisa", "english": "justice, fairness"},
    {"type": "noun", "swedish": "myndighet", "english": "authority, agency"},
    {"type": "noun", "swedish": "polis", "english": "police"},
    {"type": "noun", "swedish": "domstol", "english": "court"},
    {"type": "noun", "swedish": "brott", "english": "crime"},
    {"type": "noun", "swedish": "straff", "english": "punishment"},
    {"type": "noun", "swedish": "invånare", "english": "inhabitant, resident"},
    {"type": "noun", "swedish": "kommun", "english": "municipality"},
    {"type": "noun", "swedish": "stat", "english": "state"},
    {"type": "noun", "swedish": "skattebetalare", "english": "taxpayer"},
    {"type": "noun", "swedish": "socialt stöd", "english": "social support"},
    {"type": "noun", "swedish": "pension", "english": "pension"},
    {"type": "noun", "swedish": "arbetslöshet", "english": "unemployment"},
    {"type": "noun", "swedish": "ekonomi", "english": "economy"},
    {"type": "noun", "swedish": "inflation", "english": "inflation"},
    {"type": "noun", "swedish": "pris", "english": "price"},
    {"type": "noun", "swedish": "kostnad", "english": "cost"},
    {"type": "noun", "swedish": "lön", "english": "salary"},
    {"type": "noun", "swedish": "företag", "english": "company"},
    {"type": "noun", "swedish": "arbetsplats", "english": "workplace"},
    {"type": "noun", "swedish": "arbetstagare", "english": "employee"},
    {"type": "noun", "swedish": "arbetsgivare", "english": "employer"},
    {"type": "noun", "swedish": "produktion", "english": "production"},
    {"type": "noun", "swedish": "export", "english": "export"},
    {"type": "noun", "swedish": "import", "english": "import"},
    {"type": "noun", "swedish": "försäljning", "english": "sales"},
    {"type": "noun", "swedish": "handel", "english": "trade"},
    {"type": "noun", "swedish": "marknad", "english": "market"},
    {"type": "noun", "swedish": "investering", "english": "investment"},
    {"type": "noun", "swedish": "resurs", "english": "resource"},
    {"type": "noun", "swedish": "miljö", "english": "environment"},
    {"type": "noun", "swedish": "hållbarhet", "english": "sustainability"},
    {"type": "noun", "swedish": "energikälla", "english": "energy source"},
    {"type": "noun", "swedish": "nyhet", "english": "news"},
    {"type": "noun", "swedish": "media", "english": "media"},
    {"type": "noun", "swedish": "tidning", "english": "newspaper"},
    {"type": "noun", "swedish": "journalist", "english": "journalist"},
    {"type": "noun", "swedish": "rapport", "english": "report"},
    {"type": "noun", "swedish": "undersökning", "english": "survey, study"},
    {"type": "noun", "swedish": "forskning", "english": "research"},
    {"type": "noun", "swedish": "resultat", "english": "result"},
    {"type": "noun", "swedish": "förändring", "english": "change"},
    {"type": "noun", "swedish": "utveckling", "english": "development"},
    {"type": "noun", "swedish": "problem", "english": "problem"},
    {"type": "noun", "swedish": "lösning", "english": "solution"},
    {"type": "noun", "swedish": "orsak", "english": "cause"},
    {"type": "noun", "swedish": "följd", "english": "consequence"},
    {"type": "noun", "swedish": "debatt", "english": "debate"},
    {"type": "noun", "swedish": "opinion", "english": "opinion"},
    {"type": "noun", "swedish": "åsikt", "english": "point of view"},
    {"type": "noun", "swedish": "diskussion", "english": "discussion"},
    {"type": "noun", "swedish": "protest", "english": "protest"},
    {"type": "noun", "swedish": "demonstration", "english": "demonstration"},
    {"type": "noun", "swedish": "teknik", "english": "technology"},
    {"type": "noun", "swedish": "dator", "english": "computer"},
    {"type": "noun", "swedish": "mobil", "english": "mobile phone"},
    {"type": "noun", "swedish": "internet", "english": "internet"},
    {"type": "noun", "swedish": "app", "english": "app"},
    {"type": "noun", "swedish": "programvara", "english": "software"},
    {"type": "noun", "swedish": "hårdvara", "english": "hardware"},
    {"type": "noun", "swedish": "system", "english": "system"},
    {"type": "noun", "swedish": "nätverk", "english": "network"},
    {"type": "noun", "swedish": "data", "english": "data"},
    {"type": "noun", "swedish": "information", "english": "information"},
    {"type": "noun", "swedish": "säkerhet", "english": "security"},
    {"type": "noun", "swedish": "lösenord", "english": "password"},
    {"type": "noun", "swedish": "e-post", "english": "email"},
    {"type": "noun", "swedish": "meddelande", "english": "message"},
    {"type": "noun", "swedish": "hemsida", "english": "website"},
    {"type": "noun", "swedish": "sociala medier", "english": "social media"},
    {"type": "noun", "swedish": "robot", "english": "robot"},
    {"type": "noun", "swedish": "maskin", "english": "machine"},
    {"type": "noun", "swedish": "innovation", "english": "innovation"},
    {"type": "noun", "swedish": "uppfinning", "english": "invention"},
    {"type": "noun", "swedish": "artificiell intelligens", "english": "artificial intelligence"},
    {"type": "noun", "swedish": "algoritm", "english": "algorithm"},
    {"type": "noun", "swedish": "dataskydd", "english": "data protection"},
    {"type": "noun", "swedish": "digitalisering", "english": "digitalization"},
    {"type": "noun", "swedish": "cyberattack", "english": "cyberattack"},
    {"type": "noun", "swedish": "elnät", "english": "power grid"},
    {"type": "noun", "swedish": "elbil", "english": "electric car"},
    {"type": "noun", "swedish": "utvecklare", "english": "developer"},
    {"type": "noun", "swedish": "plattform", "english": "platform"},
    {"type": "noun", "swedish": "kris", "english": "crisis"},
    {"type": "noun", "swedish": "konflikt", "english": "conflict"},
    {"type": "noun", "swedish": "fred", "english": "peace"},
    {"type": "noun", "swedish": "krig", "english": "war"},
    {"type": "noun", "swedish": "flykting", "english": "refugee"},
    {"type": "noun", "swedish": "invandring", "english": "immigration"},
    {"type": "noun", "swedish": "integration", "english": "integration"},
    {"type": "noun", "swedish": "samhällsproblem", "english": "social issue"},
    {"type": "noun", "swedish": "lösning", "english": "solution"},
    {"type": "noun", "swedish": "framtid", "english": "future"},
    {"type": "noun", "swedish": "påverkan", "english": "impact"},
    {"type": "noun", "swedish": "lösning", "english": "solution"},
    {"type": "noun", "swedish": "omställning", "english": "transition/conversion"},
    {"type": "noun", "swedish": "utbildning", "english": "training"},
    {"type": "noun", "swedish": "yrkesverksamma", "english": "professionals"},
    {"type": "noun", "swedish": "subvention", "english": "subsidy"},
    {"type": "noun", "swedish": "satsning", "english": "investment"},
    {"type": "noun", "swedish": "mål", "english": "goal"},
    {"type": "noun", "swedish": "färdighet", "english": "skill"},
    förnybar:  renewable
    på grund av: because of
]

all_verbs = [
    {"type": "verb", "infinitive": "påverka",
        "english": "affect",
        "present": "påverkar",
        "past": "påverkade",
        "supine": "påverkat",
        "imperative": "påverka",
        "passive": "påverkas",
        "adjective form": "påverkad"
    },
    {"type": "verb", "infinitive": "bestämma",
        "english": "decide/determine",
        "present": "bestämmer",
        "past": "bestämde",
        "supine": "bestämt",
        "imperative": "bestäm",
        "passive": "bestäms",
        "adjective form": "bestämd"
    },
    {"type": "verb", "infinitive": "styra",
        "english": "govern/control",
        "present": "styr",
        "past": "styrde",
        "supine": "styrt",
        "imperative": "styr",
        "passive": "styrs",
        "adjective form": "styrd"
    },
    {"type": "verb", "infinitive": "leda",
        "english": "lead",
        "present": "leder",
        "past": "ledde",
        "supine": "lett",
        "imperative": "led",
        "passive": "leds",
        "adjective form": "ledd"
    },
    {"type": "verb", "infinitive": "förändra",
        "english": "change",
        "present": "förändrar",
        "past": "förändrade",
        "supine": "förändrat",
        "imperative": "förändra",
        "passive": "förändras",
        "adjective form": "förändrad"
    },
    {"type": "verb", "infinitive": "utveckla",
        "english": "develop",
        "present": "utvecklar",
        "past": "utvecklade",
        "supine": "utvecklat",
        "imperative": "utveckla",
        "passive": "utvecklas",
        "adjective form": "utvecklad"
    },
    {"type": "verb", "infinitive": "bygga",
        "english": "build",
        "present": "bygger",
        "past": "byggde",
        "supine": "byggt",
        "imperative": "bygg",
        "passive": "byggs",
        "adjective form": "byggd"
    },
    {"type": "verb", "infinitive": "skapa",
        "english": "create",
        "present": "skapar",
        "past": "skapade",
        "supine": "skapat",
        "imperative": "skapa",
        "passive": "skapas",
        "adjective form": "skapad"
    },
    {"type": "verb", "infinitive": "förbättra",
        "english": "improve",
        "present": "förbättrar",
        "past": "förbättrade",
        "supine": "förbättrat",
        "imperative": "förbättra",
        "passive": "förbättras",
        "adjective form": "förbättrad"
    },
    {"type": "verb", "infinitive": "minska",
        "english": "reduce",
        "present": "minskar",
        "past": "minskade",
        "supine": "minskat",
        "imperative": "minska",
        "passive": "minskas",
        "adjective form": "minskad"
    },
    {"type": "verb", "infinitive": "öka",
        "english": "increase",
        "present": "ökar",
        "past": "ökade",
        "supine": "ökat",
        "imperative": "öka",
        "passive": "ökas",
        "adjective form": "ökad"
    },
    {"type": "verb", "infinitive": "använda",
        "english": "use",
        "present": "använder",
        "past": "använde",
        "supine": "använt",
        "imperative": "använd",
        "passive": "användes",
        "adjective form": "använd"
    },
    {"type": "verb", "infinitive": "producera",
        "english": "produce",
        "present": "producerar",
        "past": "producerade",
        "supine": "producerat",
        "imperative": "producera",
        "passive": "produceras",
        "adjective form": "producerad"
    },
    {"type": "verb", "infinitive": "förbjuda",
        "english": "prohibit",
        "present": "förbjuder",
        "past": "förbjöd",
        "supine": "förbjudit",
        "imperative": "förbjud",
        "passive": "förbjuds",
        "adjective form": "förbjuden"
    },
    {"type": "verb", "infinitive": "tillåta",
        "english": "allow/permit",
        "present": "tillåter",
        "past": "tillät",
        "supine": "tillåtit",
        "imperative": "tillåt",
        "passive": "tillåts",
        "adjective form": "tillåten"
    },
    {"type": "verb", "infinitive": "diskutera",
        "english": "discuss",
        "present": "diskuterar",
        "past": "diskuterade",
        "supine": "diskuterat",
        "imperative": "diskutera",
        "passive": "diskuteras",
        "adjective form": "diskuterad"
    },
    {"type": "verb", "infinitive": "besluta",
        "english": "decide",
        "present": "beslutar",
        "past": "beslutade",
        "supine": "beslutat",
        "imperative": "besluta",
        "passive": "beslutas",
        "adjective form": "beslutat"
    },
    {"type": "verb", "infinitive": "rösta",
        "english": "vote",
        "present": "röstar",
        "past": "röstade",
        "supine": "röstat",
        "imperative": "rösta",
        "passive": "röstas",
        "adjective form": "röstad"
    },
    {"type": "verb", "infinitive": "arbeta",
        "english": "work",
        "present": "arbetar",
        "past": "arbetade",
        "supine": "arbetat",
        "imperative": "arbeta",
        "passive": "arbetas",
        "adjective form": "arbetad"
    },
    {"type": "verb", "infinitive": "tjäna",
        "english": "earn (money)",
        "present": "tjänar",
        "past": "tjänade",
        "supine": "tjänat",
        "imperative": "tjäna",
        "passive": "tjänades",
        "adjective form": "intjänad"
    },
    {"type": "verb", "infinitive": "betala",
        "english": "pay",
        "present": "betalar",
        "past": "betalade",
        "supine": "betalat",
        "imperative": "betala",
        "passive": "betalades",
        "adjective form": "betalad"
    },
    {"type": "verb", "infinitive": "spara",
        "english": "save (money)",
        "present": "sparar",
        "past": "sparade",
        "supine": "sparat",
        "imperative": "spara",
        "passive": "sparades",
        "adjective form": "sparad"
    },
    {"type": "verb", "infinitive": "investera",
        "english": "invest",
        "present": "investerar",
        "past": "investerade",
        "supine": "investerat",
        "imperative": "investera",
        "passive": "investeras",
        "adjective form": "investerad"
    },
    {"type": "verb", "infinitive": "forska",
        "english": "research",
        "present": "forskar",
        "past": "forskade",
        "supine": "forskat",
        "imperative": "forska",
        "passive": "forskas",
        "adjective form": "forskad"
    },
    {"type": "verb", "infinitive": "uppfinna",
        "english": "invent",
        "present": "uppfinner",
        "past": "uppfann",
        "supine": "uppfunnit",
        "imperative": "uppfinn",
        "passive": "uppfinns",
        "adjective form": "uppfunnen"
    },
    {"type": "verb", "infinitive": "förklara",
        "english": "explain",
        "present": "förklarar",
        "past": "förklarade",
        "supine": "förklarat",
        "imperative": "förklara",
        "passive": "förklarades",
        "adjective form": "förklarad"
    },
    {"type": "verb", "infinitive": "informera",
        "english": "inform",
        "present": "informerar",
        "past": "informerade",
        "supine": "informerat",
        "imperative": "informera",
        "passive": "informeras",
        "adjective form": "informerad"
    },
    {"type": "verb", "infinitive": "rapportera",
        "english": "report",
        "present": "rapporterar",
        "past": "rapporterade",
        "supine": "rapporterat",
        "imperative": "rapportera",
        "passive": "rapporterades",
        "adjective form": "rapporterad"
    },
    {"type": "verb", "infinitive": "kontrollera",
        "english": "check/verify",
        "present": "kontrollerar",
        "past": "kontrollerade",
        "supine": "kontrollerat",
        "imperative": "kontrollera",
        "passive": "kontrollerades",
        "adjective form": "kontrollerad"
    },
    {"type": "verb", "infinitive": "övervaka",
        "english": "monitor/oversee",
        "present": "övervakar",
        "past": "övervakade",
        "supine": "övervakat",
        "imperative": "övervaka",
        "passive": "övervakades",
        "adjective form": "övervakad"
    },
    {"type": "verb", "infinitive": "försvara",
        "english": "defend/justify",
        "present": "försvarar",
        "past": "försvarade",
        "supine": "försvarat",
        "imperative": "försvara",
        "passive": "försvarades",
        "adjective form": "försvarad"
    },
    {"type": "verb", "infinitive": "skydda",
        "english": "protect",
        "present": "skyddar",
        "past": "skyddade",
        "supine": "skyddat",
        "imperative": "skydda",
        "passive": "skyddades",
        "adjective form": "skyddad"
    },
    {"type": "verb", "infinitive": "hjälpa",
        "english": "help",
        "present": "hjälper",
        "past": "hjälpte",
        "supine": "hjälpt",
        "imperative": "hjälp",
        "passive": "",
        "adjective form": "hjälpt"
    },
    {"type": "verb", "infinitive": "påminna",
        "english": "remind",
        "present": "påminner",
        "past": "påminde",
        "supine": "påmint",
        "imperative": "påminn",
        "passive": "påminns",
        "adjective form": "påmind"
    },
    {"type": "verb", "infinitive": "stöda",
        "english": "support",
        "present": "stöder",
        "past": "stödde",
        "supine": "stött",
        "imperative": "stöd",
        "passive": "stöds",
        "adjective form": "stödd"
    },
    {"type": "verb", "infinitive": "tillhöra",
        "english": "belong",
        "present": "tillhör",
        "past": "tillhörde",
        "supine": "tillhört",
        "imperative": "tillhör",
        "passive": "",
        "adjective form": "tillhörande"
    },
    {"type": "verb", "infinitive": "tro",
        "english": "believe",
        "present": "tror",
        "past": "trodde",
        "supine": "trott",
        "imperative": "tro",
        "passive": "tros",
        "adjective form": "trodd"
    },
    {"type": "verb", "infinitive": "tycka",
        "english": "think",
        "present": "tycker",
        "past": "tyckte",
        "supine": "tyckt",
        "imperative": "tyck",
        "passive": "tycks"
    },
    {"type": "verb", "infinitive": "anse",
        "english": "consider",
        "present": "anser",
        "past": "ansåg",
        "supine": "ansett",
        "imperative": "anse",
        "passive": "anses",
        "adjective form": ""
    },
    {"type": "verb", "infinitive": "hålla med",
        "english": "agree",
        "present": "håller",
        "past": "höll",
        "supine": "hållit",
        "imperative": "håll",
        "passive": "",
        "adjective form": ""
    },
    {"type": "verb", "infinitive": "försvinna",
        "english": "disappear",
        "present": "försvinner",
        "past": "försvann",
        "supine": "försvunnit",
        "imperative": "försvinna",
        "passive": "",
        "adjective form": "försvunnen"
    },
    {"type": "verb", "infinitive": "ersätta",
        "english": "replace",
        "present": "ersätter",
        "past": "ersatte",
        "supine": "ersatt",
        "imperative": "ersätt",
        "passive": "ersattes",
        "adjective form": "ersatt"
    },
    {"type": "verb", "infinitive": "påpeka",
        "english": "point out",
        "present": "påpekar",
        "past": "påpekade",
        "supine": "påpekat",
        "imperative": "påpeka",
        "passive": "påpekades",
        "adjective form": "påpekad"
    },
    {"type": "verb", "infinitive": "nå",
        "english": "reach/gain (business)",
        "present": "når",
        "past": "nådde",
        "supine": "nått",
        "imperative": "nå",
        "passive": "nås",
        "adjective form": "nådd"
    },
    {"type": "verb", "infinitive": "underlätta",
        "english": "facilitate",
        "present": "underlättar",
        "past": "underlätterade",
        "supine": "underlätt",
        "imperative": "underlätta",
        "passive": "underlättades",
        "adjective form": "underlättad"
    },
    {"type": "verb", "infinitive": "förbli",
        "english": "remain",
        "present": "förblir",
        "past": "förblev",
        "supine": "förblivit",
        "imperative": "förbliv",
        "passive": "",
        "adjective form": ""
    }
]

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

START_SIZE = 5        # how many of each to start with
UNLOCK_BATCH = 3      # how many new words to add when unlocking
MASTERY_THRESHOLD = 0.6  # proportion correct required
MIN_ATTEMPTS = 3      # need at least this many attempts to count

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

    else:
        # Aggregate all tenses for the verb
        total_asked = total_correct = 0
        for t in ["infinitive", "present", "past", "supine", "imperative"]:
            key = f"verb-{entry['infinitive']}-{t}"
            rec = stats.get(key, {"asked": 0, "correct": 0})
            total_asked += rec["asked"]
            total_correct += rec["correct"]

        if total_asked < MIN_ATTEMPTS * 2:  # need a few total attempts
            return False

        acc = total_correct / total_asked if total_asked else 0
        return acc >= MASTERY_THRESHOLD

def update_active_words():
    global active_nouns, active_verbs

    mastered_nouns = sum(is_mastered(n) for n in active_nouns)
    mastered_verbs = sum(is_mastered(v) for v in active_verbs)

    if mastered_nouns == len(active_nouns) and len(active_nouns) < len(all_nouns):
        next_n = min(len(all_nouns), len(active_nouns) + UNLOCK_BATCH)
        active_nouns = all_nouns[:next_n]
        print(f"🌱 Added {next_n - len(active_nouns)} new nouns! Total active: {len(active_nouns)}")

    if mastered_verbs == len(active_verbs) and len(active_verbs) < len(all_verbs):
        next_v = min(len(all_verbs), len(active_verbs) + UNLOCK_BATCH)
        active_verbs = all_verbs[:next_v]
        print(f"🌱 Added {next_v - len(active_verbs)} new verbs! Total active: {len(active_verbs)}")

# ===============================
#  QUIZ FUNCTIONS
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

print("=== 🇸🇪 Society Vocabulary Trainer ===")
print("Mix of nouns and verbs (adaptive + progressive)")
print("Ctrl+C to quit.\n")

try:
    while True:
        choice_type = random.choice(["noun", "verb"])
        if choice_type == "noun" and active_nouns:
            weights = [get_weight(n) for n in active_nouns]
            noun = random.choices(active_nouns, weights=weights, k=1)[0]
            ask_noun(noun)
        elif active_verbs:
            weighted = []
            for v in active_verbs:
                for tense in ["infinitive", "present", "past", "supine", "imperative"]:
                    weighted.append((v, tense, get_weight(v, tense)))
            (verb, tense, _) = random.choices(weighted, weights=[w for _, _, w in weighted], k=1)[0]
            ask_verb(verb)

except KeyboardInterrupt:
    print("\n👋 Goodbye! Lycka till med din svenska!")
    save_stats()