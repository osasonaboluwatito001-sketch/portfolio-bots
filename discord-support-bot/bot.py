"""Discord support bot: /faq, /ticket, /help and keyword auto-answers."""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

import discord
from discord import app_commands
from dotenv import load_dotenv

BASE = Path(__file__).parent
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
log = logging.getLogger("support-bot")

with open(BASE / "faq.json", encoding="utf-8") as f:
    FAQ: dict = json.load(f)


def find_faq(text: str) -> str | None:
    t = text.lower()
    for topic, item in FAQ.items():
        if any(k in t for k in item["keywords"]):
            return topic
    return None


class SupportBot(discord.Client):
    def __init__(self, support_channel_id: int | None, guild_id: int | None):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.support_channel_id = support_channel_id
        self.guild_id = guild_id

    async def setup_hook(self) -> None:
        if self.guild_id:
            guild = discord.Object(id=self.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def on_ready(self) -> None:
        log.info("Logged in as %s", self.user)

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.channel.id != self.support_channel_id:
            return
        topic = find_faq(message.content)
        if topic:
            await message.reply(f"💡 **{topic}**: {FAQ[topic]['answer']}", mention_author=False)


def build_bot(support_channel_id: int | None, guild_id: int | None) -> SupportBot:
    bot = SupportBot(support_channel_id, guild_id)

    async def topic_autocomplete(_: discord.Interaction, current: str):
        return [app_commands.Choice(name=t, value=t) for t in FAQ if current.lower() in t][:25]

    @bot.tree.command(name="faq", description="Get an answer to a common question")
    @app_commands.autocomplete(topic=topic_autocomplete)
    async def faq_cmd(interaction: discord.Interaction, topic: str):
        key = topic if topic in FAQ else find_faq(topic)
        if key:
            await interaction.response.send_message(f"💡 **{key}**: {FAQ[key]['answer']}")
        else:
            await interaction.response.send_message(
                f"No FAQ for that. Topics: {', '.join(FAQ)}. Or open a /ticket.", ephemeral=True)

    @bot.tree.command(name="ticket", description="Open a private support thread")
    async def ticket_cmd(interaction: discord.Interaction, issue: str):
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("Use this in a server text channel.", ephemeral=True)
            return
        thread = await channel.create_thread(
            name=f"ticket-{interaction.user.display_name}"[:90],
            type=discord.ChannelType.private_thread, invitable=False)
        await thread.add_user(interaction.user)
        await thread.send(f"🎫 {interaction.user.mention} opened a ticket:\n> {issue}\nA team member will be with you soon.")
        await interaction.response.send_message(f"Ticket created: {thread.mention}", ephemeral=True)

    @bot.tree.command(name="help", description="Show what this bot can do")
    async def help_cmd(interaction: discord.Interaction):
        await interaction.response.send_message(
            "**Support Bot**\n`/faq <topic>` – quick answers\n`/ticket <issue>` – private support thread\n"
            "I also auto-answer common questions in the support channel.", ephemeral=True)

    return bot


def _int_env(name: str) -> int | None:
    v = os.getenv(name, "").strip()
    return int(v) if v.isdigit() else None


def main() -> None:
    load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        sys.exit("ERROR: DISCORD_BOT_TOKEN is not set. Copy .env.example to .env and add your token.")
    build_bot(_int_env("SUPPORT_CHANNEL_ID"), _int_env("GUILD_ID")).run(token, log_handler=None)


if __name__ == "__main__":
    main()
