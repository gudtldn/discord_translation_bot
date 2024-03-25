import discord
from discord import app_commands

from json import load


with open("./lang.json", "r", encoding="utf-8") as fr:
    localizations: dict[str, dict[str, str]] = load(fr)


class Translation(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContextTypes
    ) -> str | None:
        msg = string.message

        if localizations.get(locale.value) is None:
            return localizations['en'][msg]

        else:
            return localizations[locale.value][msg]
