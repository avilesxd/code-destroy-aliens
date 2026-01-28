# 🌍 Translations Guide

## Overview

Translations are stored as JSON files in `src/assets/translations/` and loaded
by the `Language` class at runtime.

## File Format

Each translation file uses a simple key/value structure:

```json
{
    "play": "Play",
    "score": "Score",
    "high_score": "High Score"
}
```

## Supported Languages

The project currently includes 46 languages:

- en — English
- es — Español
- fr — Français
- de — Deutsch
- it — Italiano
- pt — Português
- ar — العربية
- bg — Български
- bn — বাংলা
- ca — Català
- cs — Čeština
- da — Dansk
- el — Ελληνικά
- eu — Euskera
- fa — فارسی
- fi — Suomi
- gl — Galego
- he — עברית
- hi — हिन्दी
- hr — Hrvatski
- hu — Magyar
- id — Bahasa Indonesia
- ja — 日本語
- kn — ಕನ್ನಡ
- ko — 한국어
- ml — മലയാളം
- ms — Bahasa Melayu
- nl — Nederlands
- no — Norsk
- pl — Polski
- ro — Română
- ru — Русский
- sk — Slovenčina
- sr — Српски
- sv — Svenska
- sw — Kiswahili
- ta — தமிழ்
- te — తెలుగు
- th — ไทย
- tl — Tagalog
- tr — Türkçe
- uk — Українська
- ur — اردو
- vi — Tiếng Việt
- zh — 中文
- zh-TW — 繁體中文

## Adding a Translation

1. Create a new `xx.json` file in `src/assets/translations/`.
2. Add the language code to `SUPPORTED_LANGUAGES`.
3. Ensure all keys match those in `en.json`.

## Quality Guidelines

- Use UTF-8 encoding.
- Keep terminology consistent across languages.
- Verify keys exist in every file.

## Related Documentation

- [Language System Guide](language_system.md)
