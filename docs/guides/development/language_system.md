# Language System Guide

This guide explains how to use and extend the game's internationalization
system.

## Overview

The language system provides a robust way to handle multiple languages in the
game, with automatic language detection and fallback mechanisms.

## Features

- Automatic system language detection
- Support for multiple languages (English, Spanish, French, German, Italian,
  Portuguese)
- Dynamic translation file loading
- Fallback to English when a translation is not available
- Simple API for retrieving translated texts

## Quick Start

### Basic Usage

```python
from src.config.language import Language

# Create a language system instance
language = Language()

# Get a translated text
text = language.get_text("play")  # Returns "Play" in English

# Change language
language.set_language("es")
text = language.get_text("play")  # Returns "Jugar" in Spanish
```

### Available Methods

```python
# Change to a supported language
success = language.set_language("fr")  # Returns True

# Try to change to an unsupported language
success = language.set_language("ru")  # Returns False

# Get list of available languages
available_languages = language.get_available_languages()
# ['en', 'es', 'fr', 'de', 'it', 'pt']
```

## Implementation Details

### File Structure

Translation files are stored in `src/assets/translations/` with the following
structure:

```
src/assets/translations/
├── en.json  # English
├── es.json  # Spanish
├── fr.json  # French
├── de.json  # German
├── it.json  # Italian
└── pt.json  # Portuguese
```

### Translation File Format

Each translation file should be a JSON file with the following format:

```json
{
    "game_controls": "Game Controls",
    "move_left_right": "Move left/right",
    "shoot": "Shoot"
    // ... more translations
}
```

## Extending the System

### Adding a New Language

1. Create a new JSON file in `src/assets/translations/` with the language code
   (e.g., `ja.json` for Japanese)
2. Add the language code to `SUPPORTED_LANGUAGES` in the `Language` class
3. Ensure all translation keys are present in the new file

### Error Handling

- If a translation is not found in the current language, the English translation
  is used
- If the translation is not found in English, the original key is returned
- If no translation files can be loaded, default English translations are used

## Best Practices

### Key Naming

- Use descriptive, lowercase keys
- Use underscores for spaces
- Keep keys consistent across all language files

### Translation Quality

- Ensure translations are accurate and natural
- Consider cultural context
- Maintain consistent terminology

### File Management

- Keep translation files organized
- Use UTF-8 encoding
- Validate JSON syntax

### Testing

- Test all supported languages
- Verify fallback behavior
- Check for missing translations

## Technical Details

### Language Detection

The system automatically detects the user's system language using the `locale`
module. If the detected language is not supported, it defaults to English.

### Translation Loading

Translation files are loaded during initialization. Each file is validated to
ensure it contains all required keys. If a file is missing or invalid, the
system falls back to default English translations.

### Performance Considerations

- Translation files are loaded once during initialization
- Text lookups are performed using dictionary access for optimal performance
- The system uses a simple key-value structure for efficient storage and
  retrieval

## Contributing

When adding new translations or modifying existing ones:

1. Ensure all keys are present in all language files
2. Maintain consistent style in translations
3. Verify translations are culturally appropriate
4. Update documentation if necessary

## Related Documentation

- [Testing Guide](../testing/README.md) - For information about testing the
  language system
