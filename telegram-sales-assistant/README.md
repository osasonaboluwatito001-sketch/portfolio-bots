# Telegram Sales Assistant

A lightweight, intentionally simple shop assistant for a generic digital-goods store, built with **python-telegram-bot v20+**.

## Features
- `/start` greeting, `/catalog` with inline product buttons, `/faq`
- Products loaded from `products.json`, FAQ answers from `faq.json`
- Keyword-based intent matching (delivery, payment, refunds, catalog)
- "Talk to a human" handoff — tells the user a seller will reply

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your token from @BotFather
python bot.py
```

## Environment variables
| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | yes | Bot token from @BotFather |
| `STORE_NAME` | no | Display name (default "Demo Digital Store") |

## Example conversation
```
User: /start
Bot:  👋 Welcome to Demo Digital Store!
      /catalog – browse products ...
User: /catalog
Bot:  🛒 Our products:
      [Chess Premium – 1 month · $4.99]
      [Chess Premium – 12 months · $39.99]
      [💬 Talk to a human]
User: (taps Chess Premium – 1 month)
Bot:  Chess Premium – 1 month
      Premium membership for an online chess platform, 1 month.
      Price: $4.99   [✅ I want this]
User: how long does delivery take?
Bot:  Digital codes are usually delivered within 5–30 minutes after payment is confirmed.
User: can I talk to a human?
Bot:  👤 Got it! A seller has been notified and will reply to you here shortly.
```

Prices and products are placeholders. MIT licensed.
