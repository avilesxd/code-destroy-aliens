import json
import locale
import os
import subprocess
import sys
from typing import Dict, Final, List

from src.core.path_utils import resource_path


class Language:
    """Handles game language and translations.

    This class manages the game's internationalization system, providing support for
    multiple languages and handling translation loading, language detection, and text
    retrieval.

    Attributes:
        SUPPORTED_LANGUAGES (List[str]): List of supported language codes.
        DEFAULT_LANGUAGE (str): Default language code to use when system language is not supported.
        TRANSLATIONS_DIR (str): Directory path where translation files are stored.

    Example:
        >>> language = Language()
        >>> text = language.get_text("play")  # Returns "Play" in English
        >>> language.set_language("es")
        >>> text = language.get_text("play")  # Returns "Jugar" in Spanish
    """

    # Constants for supported languages
    SUPPORTED_LANGUAGES: Final[List[str]] = ["en", "es", "fr", "de", "it", "pt", "ar", "bg"]
    DEFAULT_LANGUAGE: Final[str] = "en"
    TRANSLATIONS_DIR: Final[str] = "src/assets/translations"

    def __init__(self) -> None:
        """Initialize language settings.

        The initialization process:
        1. Sets the program's locale to the user's default system settings.
        2. Detects the system language based on the new locale.
        3. Loads all available translations.
        4. Sets the current language.
        """
        try:
            # Set the locale to the user's default setting. This is a best-effort
            # attempt, but can be unreliable on macOS for GUI apps.
            locale.setlocale(locale.LC_ALL, "")
        except locale.Error:
            # This can fail if the user's locale is not supported by the OS.
            print("Warning: Failed to set the system's default locale.")

        self.system_language = self._get_system_language()
        self.translations = self._load_translations()
        self.current_language = self._get_supported_language()

    def _get_system_language(self) -> str:
        """Get the system language code by trying platform-specific methods."""
        if sys.platform == "darwin":
            lang = self._get_macos_language()
            if lang:
                return lang

        # Fallback for non-macOS systems or if the macOS method fails.
        lang = self._get_fallback_language()
        if lang:
            return lang

        return self.DEFAULT_LANGUAGE

    def _get_macos_language(self) -> str | None:
        """Directly queries macOS for its preferred language."""
        try:
            command = ["defaults", "read", "-g", "AppleLanguages"]
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding="utf-8")
            output = result.stdout.strip()

            if output.startswith("(") and ")" in output:
                first_quote = output.find('"')
                if first_quote != -1:
                    second_quote = output.find('"', first_quote + 1)
                    if second_quote != -1:
                        lang_region = output[first_quote + 1 : second_quote]
                        lang_code = lang_region.split("-")[0]
                        if len(lang_code) == 2:
                            return lang_code.lower()
        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
            return None
        return None

    def _get_fallback_language(self) -> str | None:
        """Gets language using the standard locale module."""
        try:
            system_locale, _ = locale.getdefaultlocale()
            if system_locale:
                lang_code = system_locale.split("_")[0]
                if len(lang_code) == 2:
                    return lang_code.lower()
        except Exception:
            return None
        return None

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load all available translations from JSON files.

        Loads translation files from the translations directory. Each file should be
        named with its language code (e.g., 'en.json', 'es.json').

        Returns:
            Dict[str, Dict[str, str]]: Dictionary mapping language codes to their translations.

        Raises:
            FileNotFoundError: If the translations directory doesn't exist.
            ValueError: If no translation files are found.
        """
        translations: Dict[str, Dict[str, str]] = {}
        try:
            translations_dir = resource_path(self.TRANSLATIONS_DIR)

            if not os.path.exists(translations_dir):
                raise FileNotFoundError(f"Translations directory not found: {translations_dir}")

            for filename in os.listdir(translations_dir):
                if filename.endswith(".json"):
                    language_code = filename.split(".")[0]
                    if language_code in self.SUPPORTED_LANGUAGES:
                        file_path = os.path.join(translations_dir, filename)
                        with open(file_path, "r", encoding="utf-8") as f:
                            translations[language_code] = json.load(f)

            if not translations:
                raise ValueError("No translation files found")

        except Exception as e:
            print(f"Error loading translations: {e}")
            translations[self.DEFAULT_LANGUAGE] = self._get_default_translations()

        return translations

    def _get_supported_language(self) -> str:
        """Get the best supported language based on system language.

        Returns:
            str: Language code that best matches the system language,
                 or default language if system language is not supported.
        """
        return self.system_language if self.system_language in self.SUPPORTED_LANGUAGES else self.DEFAULT_LANGUAGE

    def _get_default_translations(self) -> Dict[str, str]:
        """Get default English translations.

        Returns:
            Dict[str, str]: Dictionary containing default English translations.
        """
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
            "toggle_music": "Music on/off",
            "toggle_sound": "Sound on/off",
        }

    def get_text(self, key: str) -> str:
        """Get translated text for a given key.

        Retrieves the translation for the specified key in the current language.
        If the translation is not found, falls back to English.
        If the key is not found in English, returns the key itself.

        Args:
            key (str): The translation key to look up.

        Returns:
            str: The translated text, or the key if no translation is found.

        Example:
            >>> language = Language()
            >>> language.get_text("play")  # Returns "Play" in English
            >>> language.set_language("es")
            >>> language.get_text("play")  # Returns "Jugar" in Spanish
        """
        try:
            return self.translations[self.current_language][key]
        except KeyError:
            # Fallback to English if translation is missing
            return self.translations[self.DEFAULT_LANGUAGE].get(key, key)

    def set_language(self, language_code: str) -> bool:
        """Set the current language if supported.

        Args:
            language_code (str): The language code to set (e.g., 'en', 'es', 'fr').

        Returns:
            bool: True if the language was set successfully, False otherwise.

        Example:
            >>> language = Language()
            >>> language.set_language("es")  # Returns True
            >>> language.set_language("ru")  # Returns False (unsupported language)
        """
        if language_code in self.SUPPORTED_LANGUAGES:
            self.current_language = language_code
            return True
        return False

    def get_available_languages(self) -> List[str]:
        """Get list of available languages.

        Returns:
            List[str]: List of language codes that have been successfully loaded.

        Example:
            >>> language = Language()
            >>> available = language.get_available_languages()
            >>> print(available)  # ['en', 'es', 'fr', 'de', 'it', 'pt']
        """
        return list(self.translations.keys())
