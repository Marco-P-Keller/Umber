"""The 39 App Store Connect locales and the app language each one is served by."""

# ASC locale -> language code in Localizable.xcstrings
ASC = {
    "ar-SA": "ar", "ca": "ca", "cs": "cs", "da": "da", "de-DE": "de", "el": "el",
    "en-AU": "en", "en-CA": "en", "en-GB": "en", "en-US": "en",
    "es-ES": "es", "es-MX": "es", "fi": "fi", "fr-CA": "fr", "fr-FR": "fr", "he": "he", "hi": "hi",
    "hr": "hr", "hu": "hu", "id": "id", "it": "it", "ja": "ja", "ko": "ko", "ms": "ms", "nl-NL": "nl",
    "no": "nb", "pl": "pl", "pt-BR": "pt-BR", "pt-PT": "pt-PT", "ro": "ro", "ru": "ru", "sk": "sk",
    "sv": "sv", "th": "th", "tr": "tr", "uk": "uk", "vi": "vi", "zh-Hans": "zh-Hans", "zh-Hant": "zh-Hant",
}
APP_LANGUAGES = sorted(set(ASC.values()))
RTL = {"ar", "he"}

IPHONE = "E631CD4F-3293-4D70-A81F-453107BF207E"   # iPhone 17 Pro Max, 1320x2868 (6.9")
IPAD = "2C61AA9F-1E8B-4E84-803A-DC9E7398E725"     # iPad Pro 13-inch (M5), 2064x2752
SCENES = ["focus", "mix", "timer", "sleep", "settings"]
