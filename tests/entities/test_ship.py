import pygame
import pytest

from src.config.configuration import Configuration
from src.config.music import Music
from src.config.statistics import Statistics
from src.entities.ship import Ship


@pytest.fixture
def ship() -> Ship:
    """Create a ship instance for testing."""
    pygame.init()
    screen = pygame.Surface((800, 600))
    config = Configuration()
    statistics = Statistics(config)
    music = Music()
    return Ship(config, screen, statistics, music)


def test_ship_initialization(ship: Ship) -> None:
    """Test ship initialization."""
    assert ship.rect.centerx == 400  # Screen width / 2
    assert ship.rect.bottom == 600  # Screen height
    assert ship.moving_right is False
    assert ship.moving_left is False
    assert ship.image is not None
    assert ship.rect is not None


def test_ship_movement_right(ship: Ship) -> None:
    """Test ship movement to the right."""
    ship.moving_right = True
    initial_x = ship.rect.centerx
    ship.update()
    assert ship.rect.centerx == initial_x + ship.ai_configuration.ship_speed_factor


def test_ship_movement_left(ship: Ship) -> None:
    """Test ship movement to the left."""
    ship.moving_left = True
    initial_x = ship.rect.centerx
    ship.update()
    assert ship.rect.centerx == initial_x - ship.ai_configuration.ship_speed_factor


def test_ship_screen_boundaries(ship: Ship) -> None:
    """Test ship stays within screen boundaries."""
    # Test right boundary
    ship.center = 800 - ship.rect.width
    ship.moving_right = True
    ship.update()
    assert ship.rect.right <= 800

    # Test left boundary
    ship.center = ship.rect.width
    ship.moving_left = True
    ship.update()
    assert ship.rect.left >= 0
