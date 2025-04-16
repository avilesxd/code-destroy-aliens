import pytest
import pygame
from src.config.configuration import Configuration
from src.config.statistics import Statistics
from src.config.language import Language
from src.entities.ship import Ship
from src.entities.button import Button
from src.entities.scoreboard import Scoreboard
from src.entities.controls_screen import ControlsScreen
from src.config.music import Music

@pytest.fixture
def game_setup():
    """Fixture to set up basic game components for testing."""
    pygame.init()
    config = Configuration()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    stats = Statistics(config)
    language = Language()
    return config, screen, stats, language

def test_game_initialization(game_setup):
    """Test if the game initializes correctly with basic components."""
    config, screen, stats, language = game_setup
    
    # Test configuration
    assert config.screen_width > 0
    assert config.screen_height > 0
    
    # Test screen
    assert isinstance(screen, pygame.Surface)
    
    # Test statistics
    assert isinstance(stats, Statistics)
    assert stats.score == 0
    assert stats.level == 1
    
    # Test language
    assert isinstance(language, Language)
    assert language.get_text("play") is not None

def test_ship_creation(game_setup):
    """Test if the ship is created correctly."""
    config, screen, stats, language = game_setup
    ship = Ship(config, screen)
    
    assert isinstance(ship, Ship)
    assert ship.rect.centerx == screen.get_rect().centerx
    assert ship.rect.bottom == screen.get_rect().bottom

def test_button_creation(game_setup):
    """Test if the play button is created correctly."""
    config, screen, stats, language = game_setup
    button = Button(config, screen, language.get_text("play"))
    
    assert isinstance(button, Button)
    assert button.rect.centerx == screen.get_rect().centerx
    assert button.rect.centery == screen.get_rect().centery

def test_scoreboard_creation(game_setup):
    """Test if the scoreboard is created correctly."""
    config, screen, stats, language = game_setup
    scoreboard = Scoreboard(config, screen, stats, language)
    
    assert isinstance(scoreboard, Scoreboard)
    assert scoreboard.statistics == stats
    assert scoreboard.screen == screen

def test_controls_screen_creation(game_setup):
    """Test if the controls screen is created correctly."""
    config, screen, stats, language = game_setup
    controls = ControlsScreen(config, screen, language)
    
    assert isinstance(controls, ControlsScreen)
    assert controls.screen == screen 

def test_music_initialization(game_setup):
    """Test if the music system initializes correctly."""
    config, screen, stats, language = game_setup
    music = Music()
    
    assert isinstance(music, Music)
    assert hasattr(music, 'volume')
    assert 0 <= music.volume <= 1.0

def test_level_progression(game_setup):
    """Test level progression and difficulty increase."""
    config, screen, stats, language = game_setup
    
    # Simulate completing a level
    initial_level = stats.level
    stats.level += 1
    
    assert stats.level == initial_level + 1
    assert config.alien_speed_factor > 0
    assert config.alien_points > 0

def test_high_score_update(game_setup):
    """Test high score updating."""
    config, screen, stats, language = game_setup
    
    # Set a new high score
    new_high_score = 1000
    stats.high_score = new_high_score
    
    assert stats.high_score == new_high_score
    assert stats.high_score > 0

def test_sound_effects(game_setup):
    """Test sound effect system."""
    config, screen, stats, language = game_setup
    music = Music()
    
    # Test sound effect methods
    assert hasattr(music, 'play_shoot')
    assert hasattr(music, 'play_explosion')
    assert hasattr(music, 'play_game_over')
    
    # Test sound effect objects
    assert isinstance(music.shoot_sound, pygame.mixer.Sound)
    assert isinstance(music.explosion_sound, pygame.mixer.Sound)
    assert isinstance(music.game_over_sound, pygame.mixer.Sound)
    
    # Test volume settings
    assert 0 <= music.shoot_sound.get_volume() <= 1.0
    assert 0 <= music.explosion_sound.get_volume() <= 1.0
    assert 0 <= music.game_over_sound.get_volume() <= 1.0 