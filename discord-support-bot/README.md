# Discord Support Bot

A small support bot built with **discord.py 2.x** using slash commands.

## Features
- `/faq <topic>` – answers from `faq.json` (with autocomplete)
- `/ticket <issue>` – creates a **private thread** for the user
- `/help` – command overview
- Auto-answers messages matching FAQ keywords in a configured support channel

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python bot.py
```
In the Developer Portal enable the **Message Content** intent. Invite with scopes `bot applications.commands` and permissions: Send Messages, Create Private Threads, Send Messages in Threads.

## Environment variables
| Variable | Required | Description |
|---|---|---|
| `DISCORD_BOT_TOKEN` | yes | Bot token |
| `SUPPORT_CHANNEL_ID` | no | Channel for keyword auto-answers |
| `GUILD_ID` | no | Sync commands instantly to one guild (dev) |

## Example conversation
```
#support
user:  I forgot my password, how do I reset it?
Bot:   💡 reset-password: Use 'Forgot password' on the login page; a reset link arrives within a few minutes.

user:  /faq topic:billing
Bot:   💡 billing: Billing questions: check your account dashboard → Billing.

user:  /ticket issue:App crashes on launch
Bot:   (only you) Ticket created: #ticket-user
#ticket-user (private)
Bot:   🎫 @user opened a ticket: > App crashes on launch
       A team member will be with you soon.
```
MIT licensed.
