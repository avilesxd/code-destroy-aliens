import json
import locale
import os
from typing import Optional

from src.core.path_utils import resource_path


class Language:
    """Handles game language and translations"""

    def __init__(self) -> None:
        """Initialize language settings"""
        # Get system language
        self.system_language = self._get_system_language()

        # Load translations
        self.translations = self._load_translations()

        # Set current language
        self.current_language = self._get_supported_language()

    def _get_system_language(self) -> str:
        """Get the system language code"""
        try:
            # Get system locale
            system_locale: Optional[str] = locale.getdefaultlocale()[0]
            if system_locale is not None:
                # Extract language code (e.g., 'en_US' -> 'en')
                return system_locale.split("_")[0]
        except Exception:
            pass
        # Default to English if detection fails
        return "en"

    def _load_translations(self) -> dict[str, dict[str, str]]:
        """Load all available translations"""
        translations: dict[str, dict[str, str]] = {}
        try:
            # Get the path to the translations directory
            translations_dir = resource_path("src/assets/translations")

            # Load each translation file
            for filename in os.listdir(translations_dir):
                if filename.endswith(".json"):
                    language_code = filename.split(".")[0]
                    file_path = os.path.join(translations_dir, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        translations[language_code] = json.load(f)
        except Exception as e:
            print(f"Error loading translations: {e}")
            # Ensure at least English is available
            translations["en"] = self._get_default_translations()

        return translations

    def _get_supported_language(self) -> str:
        """Get the best supported language based on system language"""
        # List of supported languages (add more as needed)
        supported_languages = ["en", "es"]

        # Try to use system language if supported
        if self.system_language in supported_languages:
            return self.system_language

        # Default to English if system language is not supported
        return "en"

    def _get_default_translations(self) -> dict[str, str]:
        """Get default English translations"""
        return {
            "game_controls": "Game Controls",
            "move_left_right": "Move left/right",
            "shoot": "Shoot",
            "pause_game": "Pause game",
            "quit_game": "Quit game",
            "press_space": "Press SPACE to continue",
            "play": "Play",
            "score": "Score",
            "high_score": "High Score",
            "level": "Level",
            "ships": "Ships",
            "game_over": "Game Over",
            "press_p": "Press 'P' to resume",
            "press_q": "Press 'Q' to quit",
        }

    def get_text(self, key: str) -> str:
        """Get translated text for a given key"""
        try:
            return self.translations[self.current_language][key]
        except KeyError:
            # Fallback to English if translation is missing
            return self.translations["en"].get(key, key)
