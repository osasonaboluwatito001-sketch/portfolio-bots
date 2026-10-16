"""Telegram sales assistant for a generic digital-goods store."""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

BASE = Path(__file__).parent
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
log = logging.getLogger("sales-assistant")

HUMAN_KEYWORDS = ("human", "seller", "agent", "person", "operator")


def load_json(name: str):
    with open(BASE / name, encoding="utf-8") as f:
        return json.load(f)


PRODUCTS = load_json("products.json")
FAQ = load_json("faq.json")
STORE = os.getenv("STORE_NAME", "Demo Digital Store")


def match_intent(text: str) -> str | None:
    """Return 'human', a FAQ topic, 'catalog' or None using simple keyword matching."""
    t = text.lower()
    if any(k in t for k in HUMAN_KEYWORDS):
        return "human"
    for topic, item in FAQ.items():
        if any(k in t for k in item["keywords"]):
            return topic
    if any(k in t for k in ("catalog", "products", "buy", "shop")):
        return "catalog"
    return None


def catalog_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(f"{p['name']} · {p['price']}", callback_data=f"p:{p['id']}")] for p in PRODUCTS]
    rows.append([InlineKeyboardButton("💬 Talk to a human", callback_data="human")])
    return InlineKeyboardMarkup(rows)


HUMAN_REPLY = "👤 Got it! A seller has been notified and will reply to you here shortly."


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"👋 Welcome to {STORE}!\n\n/catalog – browse products\n/faq – delivery, payment & refunds\n"
        "Or just ask me a question. Type 'human' anytime to reach a seller.")


async def catalog(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🛒 Our products:", reply_markup=catalog_keyboard())


async def faq(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    text = "\n\n".join(f"*{k.title()}*: {v['answer']}" for k, v in FAQ.items())
    await update.message.reply_text(text, parse_mode="Markdown")


async def on_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    await q.answer()
    if q.data == "human":
        await q.message.reply_text(HUMAN_REPLY)
        return
    pid = q.data.removeprefix("p:")
    p = next((x for x in PRODUCTS if x["id"] == pid), None)
    if not p:
        await q.message.reply_text("Sorry, that product is no longer available.")
        return
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ I want this", callback_data="human")]])
    await q.message.reply_text(f"*{p['name']}*\n{p['description']}\nPrice: {p['price']}",
                               parse_mode="Markdown", reply_markup=kb)


async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    intent = match_intent(update.message.text or "")
    if intent == "human":
        await update.message.reply_text(HUMAN_REPLY)
    elif intent == "catalog":
        await catalog(update, ctx)
    elif intent:
        await update.message.reply_text(FAQ[intent]["answer"])
    else:
        await update.message.reply_text("I'm not sure about that 🤔 Try /catalog, /faq, or type 'human'.")


def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        sys.exit("ERROR: TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env and add your token.")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalog", catalog))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    log.info("Bot starting…")
    app.run_polling()


if __name__ == "__main__":
    main()
