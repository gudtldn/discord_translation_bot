import discord
from discord.ext import commands, tasks

import os
import logging
from itertools import cycle

from classes.deepl import Deepl
from classes.translation import Translation


status = cycle(["번역", "翻訳", "Translation"])

class Bot(commands.Bot):
    def __init__(self):
        self.logger = logging.getLogger("discord.bot")
        self.deepl = Deepl(os.getenv("DEEPL_API_KEY"))

        super().__init__(
            command_prefix=".",
            help_command=None,
            status=discord.Status.online,
            intents=discord.Intents.all()
        )

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        await self.tree.set_translator(Translation())
        await self.tree.sync()

    async def on_ready(self):
        self.change_status.start()
        self.logger.info(f"{self.user}로 로그인")

    @tasks.loop(seconds=20)
    async def change_status(self):
        global status
        await self.change_presence(activity=discord.Game(next(status)))

    async def on_message(self, msg: discord.Message):
        return

    async def on_command_error(self, ctx: commands.Context["Bot"], error):
        if isinstance(error, commands.CommandNotFound):
            return
        await super().on_command_error(ctx, error)
