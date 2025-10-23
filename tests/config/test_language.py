from typing import List

import pytest

from src.config.language.language import Language


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
    assert language.get_text("game_controls") == "Game Controls"
    assert language.get_text("move_left_right") == "Move left/right"
    assert language.get_text("shoot") == "Shoot"
    assert language.get_text("pause_game") == "Pause game"
    assert language.get_text("quit_game") == "Quit game"
    assert language.get_text("press_space") == "Press SPACE to continue"
    assert language.get_text("play") == "Play"
    assert language.get_text("score") == "Score"
    assert language.get_text("high_score") == "High Score"
    assert language.get_text("level") == "Level"
    assert language.get_text("ships") == "Ships"
    assert language.get_text("game_over") == "Game Over"
    assert language.get_text("press_p") == "Press 'P' to resume"
    assert language.get_text("press_q") == "Press 'Q' to quit"
    assert language.get_text("toggle_music") == "Music on/off"
    assert language.get_text("toggle_sound") == "Sound on/off"
    assert language.get_text("paused_game") == "Paused Game"


def test_get_text_spanish(language: Language) -> None:
    """Test getting Spanish translations."""
    language.current_language = "es"
    assert language.get_text("game_controls") == "Controles del Juego"
    assert language.get_text("move_left_right") == "Mover izquierda/derecha"
    assert language.get_text("shoot") == "Disparar"
    assert language.get_text("pause_game") == "Pausar juego"
    assert language.get_text("quit_game") == "Salir del juego"
    assert language.get_text("press_space") == "Presiona ESPACIO para continuar"
    assert language.get_text("play") == "Jugar"
    assert language.get_text("score") == "Puntuación"
    assert language.get_text("high_score") == "Puntuación Máxima"
    assert language.get_text("level") == "Nivel"
    assert language.get_text("ships") == "Naves"
    assert language.get_text("game_over") == "Juego Terminado"
    assert language.get_text("press_p") == "Presiona 'P' para reanudar"
    assert language.get_text("press_q") == "Presiona 'Q' para salir"
    assert language.get_text("toggle_music") == "Música encendida/apagada"
    assert language.get_text("toggle_sound") == "Sonido encendido/apagado"
    assert language.get_text("paused_game") == "Juego en Pausa"


def test_get_text_french(language: Language) -> None:
    """Test getting French translations."""
    language.current_language = "fr"
    assert language.get_text("game_controls") == "Contrôles du Jeu"
    assert language.get_text("move_left_right") == "Déplacer gauche/droite"
    assert language.get_text("shoot") == "Tirer"
    assert language.get_text("pause_game") == "Pause"
    assert language.get_text("quit_game") == "Quitter"
    assert language.get_text("press_space") == "Appuyez sur ESPACE pour continuer"
    assert language.get_text("play") == "Jouer"
    assert language.get_text("score") == "Score"
    assert language.get_text("high_score") == "Meilleur Score"
    assert language.get_text("level") == "Niveau"
    assert language.get_text("ships") == "Vaisseaux"
    assert language.get_text("game_over") == "Partie Terminée"
    assert language.get_text("press_p") == "Appuyez sur 'P' pour reprendre"
    assert language.get_text("press_q") == "Appuyez sur 'Q' pour quitter"
    assert language.get_text("toggle_music") == "Musique on/off"
    assert language.get_text("toggle_sound") == "Son on/off"
    assert language.get_text("paused_game") == "Jeu en Pause"


def test_get_text_german(language: Language) -> None:
    """Test getting German translations."""
    language.current_language = "de"
    assert language.get_text("game_controls") == "Spielsteuerung"
    assert language.get_text("move_left_right") == "Links/Rechts bewegen"
    assert language.get_text("shoot") == "Schießen"
    assert language.get_text("pause_game") == "Spiel pausieren"
    assert language.get_text("quit_game") == "Spiel beenden"
    assert language.get_text("press_space") == "Drücke LEERTASTE zum Fortfahren"
    assert language.get_text("play") == "Spielen"
    assert language.get_text("score") == "Punktestand"
    assert language.get_text("high_score") == "Höchstpunktestand"
    assert language.get_text("level") == "Level"
    assert language.get_text("ships") == "Raumschiffe"
    assert language.get_text("game_over") == "Spiel Vorbei"
    assert language.get_text("press_p") == "Drücke 'P' zum Fortsetzen"
    assert language.get_text("press_q") == "Drücke 'Q' zum Beenden"
    assert language.get_text("toggle_music") == "Musik ein/aus"
    assert language.get_text("toggle_sound") == "Sound ein/aus"
    assert language.get_text("paused_game") == "Spiel Pausiert"


def test_get_text_italian(language: Language) -> None:
    """Test getting Italian translations."""
    language.current_language = "it"
    assert language.get_text("game_controls") == "Controlli di Gioco"
    assert language.get_text("move_left_right") == "Muovi sinistra/destra"
    assert language.get_text("shoot") == "Spara"
    assert language.get_text("pause_game") == "Pausa gioco"
    assert language.get_text("quit_game") == "Esci dal gioco"
    assert language.get_text("press_space") == "Premi SPAZIO per continuare"
    assert language.get_text("play") == "Gioca"
    assert language.get_text("score") == "Punteggio"
    assert language.get_text("high_score") == "Punteggio Massimo"
    assert language.get_text("level") == "Livello"
    assert language.get_text("ships") == "Navicelle"
    assert language.get_text("game_over") == "Gioco Finito"
    assert language.get_text("press_p") == "Premi 'P' per riprendere"
    assert language.get_text("press_q") == "Premi 'Q' per uscire"
    assert language.get_text("toggle_music") == "Musica on/off"
    assert language.get_text("toggle_sound") == "Suono on/off"
    assert language.get_text("paused_game") == "Gioco in Pausa"


def test_get_text_portuguese(language: Language) -> None:
    """Test getting Portuguese translations."""
    language.current_language = "pt"
    assert language.get_text("game_controls") == "Controles do Jogo"
    assert language.get_text("move_left_right") == "Mover esquerda/direita"
    assert language.get_text("shoot") == "Atirar"
    assert language.get_text("pause_game") == "Pausar jogo"
    assert language.get_text("quit_game") == "Sair do jogo"
    assert language.get_text("press_space") == "Pressione ESPAÇO para continuar"
    assert language.get_text("play") == "Jogar"
    assert language.get_text("score") == "Pontuação"
    assert language.get_text("high_score") == "Pontuação Máxima"
    assert language.get_text("level") == "Nível"
    assert language.get_text("ships") == "Naves"
    assert language.get_text("game_over") == "Jogo Terminado"
    assert language.get_text("press_p") == "Pressione 'P' para retomar"
    assert language.get_text("press_q") == "Pressione 'Q' para sair"
    assert language.get_text("toggle_music") == "Música on/off"
    assert language.get_text("toggle_sound") == "Som on/off"
    assert language.get_text("paused_game") == "Jogo em Pausa"


def test_get_text_arabic(language: Language) -> None:
    """Test getting Portuguese translations."""
    language.current_language = "ar"
    assert language.get_text("game_controls") == "عناصر التحكم في اللعبة"
    assert language.get_text("move_left_right") == "تحرك يسارًا/يمينًا"
    assert language.get_text("shoot") == "أطلق النار"
    assert language.get_text("pause_game") == "إيقاف اللعبة مؤقتًا"
    assert language.get_text("quit_game") == "إنهاء اللعبة"
    assert language.get_text("press_space") == "اضغط على SPACE للمتابعة"
    assert language.get_text("play") == "لعب"
    assert language.get_text("score") == "النتيجة"
    assert language.get_text("high_score") == "أعلى نتيجة"
    assert language.get_text("level") == "المستوى"
    assert language.get_text("ships") == "السفن"
    assert language.get_text("game_over") == "انتهت اللعبة"
    assert language.get_text("press_p") == "اضغط على 'P' للاستئناف"
    assert language.get_text("press_q") == "اضغط على 'Q' للخروج"
    assert language.get_text("toggle_music") == "تبديل الموسيقى"
    assert language.get_text("toggle_sound") == "تبديل الصوت"
    assert language.get_text("paused_game") == "اللعبة متوقفة مؤقتا"


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
        "paused_game",
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
