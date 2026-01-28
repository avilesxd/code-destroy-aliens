# 🌐 Language System Guide

## Overview

The language system provides automatic language detection and translation lookup
via the `Language` class in `src/config/language/language.py`.

## Features

- Automatic system language detection (with OS-specific fallbacks)
- 46 supported languages
- Fallback to English for missing keys
- JSON-based translation files

## Basic Usage

```python
from src.config.language.language import Language

language = Language()
text = language.get_text("play")
language.set_language("es")
```

## Supported Languages

Languages are defined in `SUPPORTED_LANGUAGES` and mapped to JSON files in
`src/assets/translations/`. See the [Translations Guide](translations.md) for
the full list.

## File Structure

```
src/assets/translations/
├── en.json
├── es.json
├── fr.json
└── ...
```

## Adding a Language

1. Add a new `xx.json` file under `src/assets/translations/`.
2. Add the language code to `SUPPORTED_LANGUAGES`.
3. Ensure all required keys are present.

## Error Handling

- Missing keys fall back to English.
- If translations fail to load, a default English set is used.

## Related Documentation

- [Translations Guide](translations.md)
- [Testing Guide](../testing/README.md)
