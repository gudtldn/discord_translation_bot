import deepl
import logging
from enum import Enum


class Locale(Enum):
    @staticmethod
    def from_str(locale: str) -> "Locale":
        locale = locale.lower()
        if locale not in Locale._value2member_map_: # type: ignore
            return Locale.ENGLISH
        elif locale in ("en", "en-us", "en-gb"):
            return Locale.ENGLISH
        elif locale in ("pt", "pt-pt", "pt-br"):
            return Locale.PORTUGUESE
        elif locale in ("es", "es-es"):
            return Locale.SPANISH
        elif locale in ("zh", "zh-cn", "zh-tw"):
            return Locale.CHINESE
        elif locale in ("nb", "no"):
            return Locale.NORWEGIAN
        return Locale(locale)

    BULGARIAN = "bg"
    CHINESE = "zh"
    CZECH = "cs"
    DANISH = "da"
    DUTCH = "nl"
    ENGLISH = "en-us"
    # ENGLISH = "en"  # Only usable as a source language
    # ENGLISH_AMERICAN = "en-US"  # Only usable as a target language
    # ENGLISH_BRITISH = "en-GB"  # Only usable as a target language
    ESTONIAN = "et"
    FINNISH = "fi"
    FRENCH = "fr"
    GERMAN = "de"
    GREEK = "el"
    HUNGARIAN = "hu"
    INDONESIAN = "id"
    ITALIAN = "it"
    JAPANESE = "ja"
    KOREAN = "ko"
    LATVIAN = "lv"
    LITHUANIAN = "lt"
    NORWEGIAN = "nb"
    POLISH = "pl"
    PORTUGUESE = "pt-pt"
    # PORTUGUESE = "pt"  # Only usable as a source language
    # PORTUGUESE_BRAZILIAN = "pt-BR"  # Only usable as a target language
    # PORTUGUESE_EUROPEAN = "pt-PT"  # Only usable as a target language
    ROMANIAN = "ro"
    RUSSIAN = "ru"
    SLOVAK = "sk"
    SLOVENIAN = "sl"
    SPANISH = "es"
    SWEDISH = "sv"
    TURKISH = "tr"
    UKRAINIAN = "uk"

locale_emoji = {
    Locale.BULGARIAN: "🇧🇬",
    Locale.CHINESE: "🇨🇳",
    Locale.CZECH: "🇨🇿",
    Locale.DANISH: "🇩🇰",
    Locale.DUTCH: "🇳🇱",
    Locale.ENGLISH: "🇺🇸",
    Locale.ESTONIAN: "🇪🇪",
    Locale.FINNISH: "🇫🇮",
    Locale.FRENCH: "🇫🇷",
    Locale.GERMAN: "🇩🇪",
    Locale.GREEK: "🇬🇷",
    Locale.HUNGARIAN: "🇭🇺",
    Locale.INDONESIAN: "🇮🇩",
    Locale.ITALIAN: "🇮🇹",
    Locale.JAPANESE: "🇯🇵",
    Locale.KOREAN: "🇰🇷",
    Locale.LATVIAN: "🇱🇻",
    Locale.LITHUANIAN: "🇱🇹",
    Locale.NORWEGIAN: "🇳🇴",
    Locale.POLISH: "🇵🇱",
    Locale.PORTUGUESE: "🇵🇹",
    Locale.ROMANIAN: "🇷🇴",
    Locale.RUSSIAN: "🇷🇺",
    Locale.SLOVAK: "🇸🇰",
    Locale.SLOVENIAN: "🇸🇮",
    Locale.SPANISH: "🇪🇸",
    Locale.SWEDISH: "🇸🇪",
    Locale.TURKISH: "🇹🇷",
    Locale.UKRAINIAN: "🇺🇦",
}


class Deepl():
    def __init__(self, api_key: str) -> None:
        self.logger = logging.getLogger("discord.bot.deepl")
        self._deepl = deepl.Translator(api_key)

    def translation_lang(self, text: str, target_lang: Locale) -> deepl.TextResult:
        return self._deepl.translate_text(text, target_lang=target_lang.value)

    def detect_lang(self, text: str) -> Locale:
        return Locale.from_str(self._deepl.translate_text(text[:15], target_lang="en-US").detected_source_lang)
