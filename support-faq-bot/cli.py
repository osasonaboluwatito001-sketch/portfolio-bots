"""Tiny interactive CLI: python cli.py  or  python cli.py "your question"."""
import os
import sys

from faq_engine import FAQEngine

FALLBACK = "Sorry, I don't know that one yet. A human will follow up."


def main() -> None:
    engine = FAQEngine.from_file(os.getenv("FAQ_PATH", "faq.json"), float(os.getenv("FAQ_THRESHOLD", "0.5")))
    if len(sys.argv) > 1:
        m = engine.ask(" ".join(sys.argv[1:]))
        print(m.answer if m else FALLBACK)
        return
    print("FAQ bot – type a question (Ctrl+D to quit)")
    try:
        while True:
            q = input("> ").strip()
            if q:
                m = engine.ask(q)
                print(f"{m.answer}  (matched: {m.question!r}, score {m.score})" if m else FALLBACK)
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
