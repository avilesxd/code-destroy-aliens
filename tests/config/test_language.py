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
    assert language.current_language in Language.SUPPORTED_LANGUAGES
    assert isinstance(language.translations, dict)
    for lang in Language.SUPPORTED_LANGUAGES:
        assert lang in language.translations


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


def test_get_text_french(language: Language) -> None:
    """Test getting French translations."""
    language.current_language = "fr"
    assert language.get_text("play") == "Jouer"
    assert language.get_text("score") == "Score"
    assert language.get_text("game_over") == "Partie Terminée"


def test_get_text_german(language: Language) -> None:
    """Test getting German translations."""
    language.current_language = "de"
    assert language.get_text("play") == "Spielen"
    assert language.get_text("score") == "Punkte"
    assert language.get_text("game_over") == "Spiel Vorbei"


def test_get_text_italian(language: Language) -> None:
    """Test getting Italian translations."""
    language.current_language = "it"
    assert language.get_text("play") == "Gioca"
    assert language.get_text("score") == "Punteggio"
    assert language.get_text("game_over") == "Game Over"


def test_get_text_portuguese(language: Language) -> None:
    """Test getting Portuguese translations."""
    language.current_language = "pt"
    assert language.get_text("play") == "Jogar"
    assert language.get_text("score") == "Pontuação"
    assert language.get_text("game_over") == "Fim de Jogo"


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
    for lang in Language.SUPPORTED_LANGUAGES:
        language.system_language = lang
        assert language._get_supported_language() == lang

    # Test with unsupported language (should default to English)
    language.system_language = "ru"
    assert language._get_supported_language() == Language.DEFAULT_LANGUAGE


def test_translation_file_loading(language: Language) -> None:
    """Test if translation files are loaded correctly."""
    # Check if all required keys are present in all languages
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

    for lang in Language.SUPPORTED_LANGUAGES:
        for key in required_keys:
            assert key in language.translations[lang]
            assert isinstance(language.translations[lang][key], str)


def test_set_language(language: Language) -> None:
    """Test setting language."""
    # Test setting supported language
    assert language.set_language("es") is True
    assert language.current_language == "es"

    # Test setting unsupported language
    assert language.set_language("ru") is False
    assert language.current_language == "es"  # Should not change


def test_get_available_languages(language: Language) -> None:
    """Test getting available languages."""
    available_languages = language.get_available_languages()
    assert isinstance(available_languages, list)
    assert all(lang in Language.SUPPORTED_LANGUAGES for lang in available_languages)
    assert len(available_languages) == len(Language.SUPPORTED_LANGUAGES)
