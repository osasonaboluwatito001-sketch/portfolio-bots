# Portfolio Bots

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_Bot_API-python--telegram--bot_20-26A5E4?logo=telegram&logoColor=white)
![Discord](https://img.shields.io/badge/discord.py-2.x-5865F2?logo=discord&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST_API-000000?logo=flask&logoColor=white)
![pytest](https://img.shields.io/badge/tested_with-pytest-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

Three small, production-style chatbots that automate everyday **customer support and sales** tasks: answering FAQs, guiding buyers through a catalog, and routing issues to a human. Built to show practical bot development, clean code, and a support-first mindset.

## The bots

| Bot | What it does for a business |
|---|---|
| [Telegram Sales Assistant](telegram-sales-assistant/) | Answers buyer questions 24/7 and walks customers from catalog to purchase, with a "talk to a human" handoff. |
| [Discord Support Bot](discord-support-bot/) | Auto-answers common questions in a support channel and opens private ticket threads for real issues. |
| [Support FAQ Bot](support-faq-bot/) | A typo-tolerant FAQ engine with a CLI and REST API that any website or bot can plug into. |

## Skills demonstrated

- **Python** – modular, readable code with JSON-driven content (no code changes to update FAQs/products)
- **Telegram Bot API** – commands, inline keyboards, callback handling (python-telegram-bot v20+)
- **discord.py** – slash commands, autocomplete, private-thread ticketing
- **Flask REST API** – `POST /ask` JSON endpoint
- **Fuzzy matching** – understands misspelled questions (`difflib` + word overlap, ranked suggestions)
- **pytest** – unit-tested FAQ engine
- **Env-based secrets** – tokens loaded from environment variables / `.env`, never committed

## Sample conversations

**Telegram Sales Assistant**
```
User: /catalog
Bot:  🛒 Our products:
      [Chess Premium – 1 month · $4.99]  [💬 Talk to a human]
User: how long does delivery take?
Bot:  Digital codes are usually delivered within 5–30 minutes after payment is confirmed.
```

**Discord Support Bot**
```
user: I forgot my password, how do I reset it?
Bot:  💡 reset-password: Use 'Forgot password' on the login page.
user: /ticket issue:App crashes on launch
Bot:  Ticket created: #ticket-user (private thread)
```

**Support FAQ Bot**
```
$ python cli.py "how do i reset my pasword"
Click 'Forgot password' on the login page.  (matched: 'How do I reset my password?', score 0.83)
```

## Quick start

```bash
cd <bot-folder>            # e.g. support-faq-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # add your bot token (not needed for support-faq-bot)
python bot.py              # or: python app.py / python cli.py / pytest -q
```

Each folder has its own README with setup details. All projects are MIT licensed.
