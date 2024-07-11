import discord
from discord.ext import commands
from discord.ui import View, Select
from discord import app_commands

from classes.bot import Bot
from classes.deepl import Locale, locale_emoji


class Translate(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.ctx_menu = [
            app_commands.ContextMenu(
                name="자동번역",
                callback=self.menu_immediate_translation
            ),
            app_commands.ContextMenu(
                name="선택번역",
                callback=self.menu_translator_msg
            )
        ]
        for menu in self.ctx_menu:
            self.bot.tree.add_command(menu)

    def get_text(self, msg: discord.Message) -> str | None:
        if msg.author.id == self.bot.user.id and msg.embeds:
            return msg.embeds[0].fields[1].value
        return msg.content or None


    async def menu_immediate_translation(self, interaction: discord.Interaction, msg: discord.Message):
        if (msg_content := self.get_text(msg)) is None:
            await interaction.response.send_message(
                content=await interaction.translate(
                    string="알 수 없는 언어",
                    locale=interaction.locale
                ),
                ephemeral=True
            )
            return

        target_lang = Locale.from_str(interaction.locale.value)
        result = self.bot.deepl.translation_lang(
            text=msg_content,
            target_lang=target_lang
        )

        embed = discord.Embed()
        field1_name = await interaction.translate(
            string="원문",
            locale=interaction.locale
        )
        field2_name = await interaction.translate(
            string="번역문",
            locale=interaction.locale
        )
        detected_lang_translation = await interaction.translate(
            string=Locale.from_str(result.detected_source_lang).value,
            locale=interaction.locale
        )
        target_lang_translation = await interaction.translate(
            string=target_lang.value,
            locale=interaction.locale
        )
        embed.add_field(name=f"{field1_name} ({detected_lang_translation})", value=msg_content, inline=False)
        embed.add_field(name=f"{field2_name} ({target_lang_translation})", value=result.text, inline=False)

        await interaction.response.send_message(embed=embed)


    async def menu_translator_msg(self, interaction: discord.Interaction, msg: discord.Message):
        async def _select_callback(_interaction: discord.Interaction):
            if interaction.user.id != _interaction.user.id:
                return

            trans_text = self.bot.deepl.translation_lang(
                msg_content,
                target_lang=Locale.from_str(_interaction.data['values'][0])
            )

            embed = discord.Embed()
            field1_name = await interaction.translate(
                string="원문",
                locale=interaction.locale
            )
            field2_name = await interaction.translate(
                string="번역문",
                locale=interaction.locale
            )
            detected_lang_translation = await interaction.translate(
                string=detected_lang.value,
                locale=interaction.locale
            )
            target_lang_translation = await interaction.translate(
                string=_interaction.data['values'][0],
                locale=interaction.locale
            )
            embed.add_field(name=f"{field1_name} ({detected_lang_translation})", value=msg_content, inline=False)
            embed.add_field(name=f"{field2_name} ({target_lang_translation})", value=trans_text.text, inline=False)

            await _interaction.response.edit_message(content=None, embed=embed, view=None)


        if (msg_content := self.get_text(msg)) is None:
            await interaction.response.send_message(
                content=await interaction.translate(
                    string="알 수 없는 언어",
                    locale=interaction.locale
                ),
                ephemeral=True
            )
            return

        detected_lang = self.bot.deepl.detect_lang(msg_content)

        _locale_copy = Locale._value2member_map_.copy()
        del _locale_copy[detected_lang.value] # 번역할 언어에서 원문 언어를 제외함

        # discord.SelectOption의 Select가 25개 이상의 옵션을 가질 수 없음
        # 따라서 일부 언어를 제외함
        del _locale_copy['bg']
        del _locale_copy['cs']
        del _locale_copy['lv']
        del _locale_copy['lt']
        

        select = Select(
            placeholder=(await interaction.translate(
                string="언어선택",
                locale=interaction.locale
            )).format(
                await interaction.translate(
                    string=detected_lang.value,
                    locale=interaction.locale
                ),
                detected_lang.value
            ),
            options=[
                discord.SelectOption(
                    label="{}({})".format(
                        await interaction.translate(
                            string=_k,
                            locale=interaction.locale
                        ),
                        _k
                    ),
                    value=_k,
                    emoji=locale_emoji[_v],
                ) for _k, _v in sorted(_locale_copy.items(), key=lambda x: x[0])
            ]
        )
        select.callback = _select_callback
        view = View()
        view.add_item(select)
        view.on_error = lambda interaction, error, item: self.bot.tree.on_error(interaction, error)

        await interaction.response.send_message(view=view)


async def setup(bot: Bot):
    await bot.add_cog(Translate(bot))
