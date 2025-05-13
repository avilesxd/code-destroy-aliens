import pygame
import pytest

from src.config.configuration import Configuration
from src.config.language.language import Language
from src.config.statistics.statistics import Statistics
from src.entities.scoreboard import Scoreboard


@pytest.fixture
def scoreboard() -> Scoreboard:
    """Create a scoreboard instance for testing."""
    pygame.init()
    screen = pygame.Surface((800, 600))
    config = Configuration()
    statistics = Statistics(config)
    language = Language()
    return Scoreboard(config, screen, statistics, language)


def test_scoreboard_initialization(scoreboard: Scoreboard) -> None:
    """Test scoreboard initialization."""
    assert scoreboard.score_image is not None
    assert scoreboard.score_rect is not None
    assert scoreboard.high_score_image is not None
    assert scoreboard.high_score_rect is not None
    assert scoreboard.level_image is not None
    assert scoreboard.level_rect is not None
    assert scoreboard.ships is not None
    assert len(scoreboard.ships) == scoreboard.statistics.ships_remaining


def test_scoreboard_score_update(scoreboard: Scoreboard) -> None:
    """Test scoreboard score update."""
    initial_score = scoreboard.statistics.score
    scoreboard.statistics.score = 100
    scoreboard.prep_score()
    assert scoreboard.score_image is not None
    assert scoreboard.score_rect is not None
    assert scoreboard.score_rect.right == scoreboard.screen_rect.right - 20
    assert scoreboard.score_rect.top == 20
    # Restore initial score
    scoreboard.statistics.score = initial_score


def test_scoreboard_high_score_update(scoreboard: Scoreboard) -> None:
    """Test scoreboard high score update."""
    initial_high_score = scoreboard.statistics.high_score
    scoreboard.statistics.high_score = 1000
    scoreboard.prep_high_score()
    assert scoreboard.high_score_image is not None
    assert scoreboard.high_score_rect is not None
    assert scoreboard.high_score_rect.centerx == scoreboard.screen_rect.centerx
    assert scoreboard.high_score_rect.top == scoreboard.score_rect.top
    # Restore initial high score
    scoreboard.statistics.high_score = initial_high_score


def test_scoreboard_level_update(scoreboard: Scoreboard) -> None:
    """Test scoreboard level update."""
    initial_level = scoreboard.statistics.level
    scoreboard.statistics.level = 2
    scoreboard.prep_level()
    assert scoreboard.level_image is not None
    assert scoreboard.level_rect is not None
    assert scoreboard.level_rect.right == scoreboard.score_rect.right
    assert scoreboard.level_rect.top == scoreboard.score_rect.bottom + 10
    # Restore initial level
    scoreboard.statistics.level = initial_level


def test_scoreboard_ships_update(scoreboard: Scoreboard) -> None:
    """Test scoreboard ships update."""
    initial_ships = scoreboard.statistics.ships_remaining
    scoreboard.statistics.ships_remaining = 2
    scoreboard.prep_ships()
    assert len(scoreboard.ships) == 2
    # Verify ship positions
    ship_list = list(scoreboard.ships)
    for i, ship in enumerate(ship_list):
        assert ship.rect.x == 10 + i * ship.rect.width
        assert ship.rect.y == 10
    # Restore initial ships
    scoreboard.statistics.ships_remaining = initial_ships
