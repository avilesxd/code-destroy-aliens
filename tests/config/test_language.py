from typing import List

import pytest

from src.config.language import Language


@pytest.fixture
def language() -> Language:
    """Fixture to create a Language instance for testing."""
    return Language()


def test_language_initialization(language: Language) -> None:
    """Test if the language system initializes correctly."""
    assert isinstance(language, Language)
    assert language.current_language in ["en", "es"]
    assert isinstance(language.translations, dict)
    assert "en" in language.translations
    assert "es" in language.translations


def test_get_text_english(language: Language) -> None:
    """Test getting English translations."""
    language.current_language = "en"
    assert language.get_text("play") == "Play"
    assert language.get_text("score") == "Score"
    assert language.get_text("game_over") == "Game Over"


def test_get_text_spanish(language: Language) -> None:
    """Test getting Spanish translations."""
    language.current_language = "es"
    assert language.get_text("play") == "Jugar"
    assert language.get_text("score") == "Puntuación"
    assert language.get_text("game_over") == "Juego Terminado"


def test_missing_translation_fallback(language: Language) -> None:
    """Test fallback to English for missing translations."""
    language.current_language = "es"
    # Test with a non-existent key
    assert language.get_text("non_existent_key") == "non_existent_key"


def test_system_language_detection(language: Language) -> None:
    """Test system language detection."""
    system_language = language._get_system_language()
    assert isinstance(system_language, str)
    assert len(system_language) == 2  # Language codes are 2 characters


def test_supported_language_selection(language: Language) -> None:
    """Test supported language selection."""
    # Test with English system language
    language.system_language = "en"
    assert language._get_supported_language() == "en"

    # Test with Spanish system language
    language.system_language = "es"
    assert language._get_supported_language() == "es"

    # Test with unsupported language (should default to English)
    language.system_language = "fr"
    assert language._get_supported_language() == "en"


def test_translation_file_loading(language: Language) -> None:
    """Test if translation files are loaded correctly."""
    # Check if all required keys are present in both languages
    required_keys: List[str] = [
        "game_controls",
        "move_left_right",
        "shoot",
        "pause_game",
        "quit_game",
        "press_space",
        "play",
        "score",
        "high_score",
        "level",
        "ships",
        "game_over",
        "press_p",
        "press_q",
    ]

    for key in required_keys:
        assert key in language.translations["en"]
        assert key in language.translations["es"]
        assert isinstance(language.translations["en"][key], str)
        assert isinstance(language.translations["es"][key], str)
