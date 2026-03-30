#!/usr/bin/env python3
"""
CLI client for the Swedish Vocabulary Quiz API.

Usage:
    python quiz.py                          # default http://localhost:8000
    python quiz.py --api-url http://host:port
    QUIZ_API_URL=http://host:port python quiz.py
"""

import argparse
import os
import sys

try:
    import requests
except ImportError:
    print("Missing dependency: requests")
    print("Install with: pip install requests")
    sys.exit(1)


class QuizCLI:
    def __init__(self, base_url: str):
        self.api = base_url.rstrip("/")
        self.session = requests.Session()
        self.topic: str | None = None
        self.topic_display: str | None = None

    def _get(self, path: str, **kw):
        try:
            r = self.session.get(f"{self.api}{path}", **kw)
            if r.status_code == 404:
                body = r.json()
                print(f"\n  {body.get('detail', 'Not found')}\n")
                return None
            r.raise_for_status()
            return r.json()
        except requests.ConnectionError:
            print(f"\n  Cannot connect to {self.api}")
            print("  Is the server running?\n")
            return None
        except requests.HTTPError as e:
            print(f"\n  API error: {e}\n")
            return None

    def _post(self, path: str, **kw):
        try:
            r = self.session.post(f"{self.api}{path}", **kw)
            if r.status_code == 404:
                body = r.json()
                print(f"\n  {body.get('detail', 'Not found')}\n")
                return None
            r.raise_for_status()
            return r.json()
        except requests.ConnectionError:
            print(f"\n  Cannot connect to {self.api}\n")
            return None
        except requests.HTTPError as e:
            print(f"\n  API error: {e}\n")
            return None

    # ── Topic selection ─────────────────────────────────────────────

    def select_topic(self) -> bool:
        data = self._get("/topics")
        if not data:
            return False

        topics = data["topics"]
        print("\nAvailable topics:\n")
        for i, t in enumerate(topics, 1):
            print(f"  {i:2d}. {t['display_name']:25s} ({t['counts']['total']} words)")

        try:
            choice = input(f"\nSelect topic [1-{len(topics)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(topics):
                self.topic = topics[idx]["name"]
                self.topic_display = topics[idx]["display_name"]
                return True
        except (ValueError, EOFError):
            pass
        print("  Invalid choice.")
        return False

    # ── Main menu ───────────────────────────────────────────────────

    def show_menu(self) -> str:
        status = self._get("/learn/status", params={"topic": self.topic})
        learned = status["learned"] if status else "?"
        total = status["total"] if status else "?"

        print(f"\n{'─' * 50}")
        print(f"  {self.topic_display}  —  {learned}/{total} words learned")
        print(f"{'─' * 50}")
        print("  [L] Learn   [Q] Quiz   [S] Stats")
        print("  [T] Topic   [X] Quit\n")

        try:
            return input("> ").strip().lower()
        except EOFError:
            return "x"

    # ── Learn mode ──────────────────────────────────────────────────

    def learn_loop(self):
        print(f"\n  Learning: {self.topic_display}")
        print("  Press Enter for next word, 'b' to go back.\n")

        while True:
            data = self._post("/learn", params={"topic": self.topic})
            if not data:
                break

            word = data["word"]
            wtype = data["type"]
            prog = data["progress"]

            print(f"  ┌─ {wtype.upper()} {'─' * (40 - len(wtype))}")

            if wtype == "noun":
                print(f"  │ indefinite       {word.get('indefinite', '–')}")
                print(f"  │ definite         {word.get('definite', '–')}")
                print(f"  │ plural           {word.get('plural', '–')}")
                print(f"  │ plural definite  {word.get('plural_definite', '–')}")
            elif wtype == "verb":
                print(f"  │ infinitive  {word.get('infinitive', '–')}")
                print(f"  │ present     {word.get('present', '–')}")
                print(f"  │ past        {word.get('past', '–')}")
                print(f"  │ supine      {word.get('supine', '–')}")
                if "imperative" in word:
                    print(f"  │ imperative  {word['imperative']}")
            else:
                print(f"  │ swedish  {word.get('swedish', '–')}")

            print(f"  │")
            print(f"  │ english  {word.get('english', '–')}")

            cefr = word.get("cefr", "–")
            freq = word.get("frequency")
            freq_str = f"{freq:.1f}" if freq else "–"
            print(f"  │ CEFR {cefr}  ·  frequency {freq_str}")
            print(f"  └{'─' * 44}")
            print(f"    [{prog['learned']}/{prog['total']} learned · {prog['remaining']} remaining]")

            try:
                cmd = input("\n  ").strip().lower()
                if cmd == "b":
                    break
            except EOFError:
                break
            print()

    # ── Quiz mode ───────────────────────────────────────────────────

    def quiz_loop(self):
        print(f"\n  Quiz: {self.topic_display}")
        print("  Type 'b' anytime to go back.\n")

        while True:
            data = self._get("/quiz", params={"topic": self.topic})
            if not data:
                break

            qid = data["question_id"]
            prompt = data["prompt"]
            options = data.get("options")

            print(f"  {prompt}")

            if options:
                for i, opt in enumerate(options, 1):
                    print(f"    {i}. {opt}")
                try:
                    raw = input("  > ").strip()
                    if raw.lower() == "b":
                        break
                    idx = int(raw) - 1
                    if 0 <= idx < len(options):
                        answer = options[idx]
                    else:
                        print("  Invalid choice.\n")
                        continue
                except (ValueError, EOFError):
                    break
            else:
                try:
                    answer = input("  > ").strip()
                    if answer.lower() == "b":
                        break
                    if not answer:
                        continue
                except EOFError:
                    break

            result = self._post(f"/quiz/{qid}", json={"answer": answer})
            if not result:
                continue

            if result["correct"]:
                print("  ✓ Correct!")
            else:
                print(f"  ✗ Wrong — correct answer: {result['correct_answer']}")

            st = result["stats"]
            acc = st["correct"] / st["asked"] if st["asked"] else 0
            print(f"    ({st['correct']}/{st['asked']} · {acc:.0%})\n")

    # ── Stats ───────────────────────────────────────────────────────

    def show_stats(self):
        data = self._get("/stats")
        if not data:
            return

        print(f"\n  {'Topic':<25} {'Seen':>5} {'Asked':>6} {'Accuracy':>9}")
        print(f"  {'─' * 48}")

        for name, s in sorted(data["stats"].items()):
            acc = f"{s['accuracy']:.0%}" if s["total_asked"] else "–"
            display = name.replace("_", " ").title()
            print(f"  {display:<25} {s['words_seen']:>5} {s['total_asked']:>6} {acc:>9}")

        print()
        input("  Press Enter to continue...")

    # ── Run ─────────────────────────────────────────────────────────

    def run(self):
        print("\n  Swedish Vocabulary Quiz")
        print(f"  API: {self.api}\n")

        while True:
            if not self.topic:
                if not self.select_topic():
                    continue

            choice = self.show_menu()

            if choice == "l":
                self.learn_loop()
            elif choice == "q":
                self.quiz_loop()
            elif choice == "s":
                self.show_stats()
            elif choice == "t":
                self.topic = None
                self.topic_display = None
            elif choice == "x":
                print("\n  Hej da!\n")
                break


def main():
    parser = argparse.ArgumentParser(description="Swedish Vocabulary Quiz CLI")
    parser.add_argument(
        "--api-url",
        default=os.environ.get("QUIZ_API_URL", "http://localhost:8000"),
        help="API base URL (default: $QUIZ_API_URL or http://localhost:8000)",
    )
    args = parser.parse_args()

    cli = QuizCLI(args.api_url)
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n  Hej da!\n")


if __name__ == "__main__":
    main()
