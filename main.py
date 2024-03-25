import discord
from discord.utils import stream_supports_colour, _ColourFormatter

import os
import dotenv
import logging
from logging.handlers import TimedRotatingFileHandler

from classes.bot import Bot

dotenv.load_dotenv()


# 스트림 로그 설정
stream_handler = logging.StreamHandler()
if isinstance(stream_handler, logging.StreamHandler) and stream_supports_colour(stream_handler.stream):
    formatter = _ColourFormatter()
else:
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}",
        dt_fmt,
        style="{"
    )
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)


# 파일 로그 설정
file_handler = TimedRotatingFileHandler(
    filename=f"./logs/latest.log",
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter(
        fmt="[{asctime}] {levelname:<8} <{name}> [{funcName} | {lineno}] >> {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    )
)
file_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(file_handler)


bot = Bot()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction[Bot], error: discord.app_commands.AppCommandError) -> None:
    bot.logger.error(error)
    translate_content = await interaction.translate(
        string="번역에러",
        locale=interaction.locale
    )
    await interaction.response.send_message(
        content=f"{translate_content}\n```{error}```"
    )

bot.run(
    token=os.environ.get("TOKEN"),
    log_handler=stream_handler,
    log_level=logging.INFO,
)
