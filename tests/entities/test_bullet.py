import pygame
import pytest

from src.config.configuration import Configuration
from src.config.statistics import Statistics
from src.entities.bullet import Bullet
from src.entities.ship import Ship


@pytest.fixture
def bullet() -> Bullet:
    """Create a bullet instance for testing."""
    pygame.init()
    ai_configuration = Configuration()
    screen = pygame.Surface((ai_configuration.screen_width, ai_configuration.screen_height))
    statistics = Statistics(ai_configuration)
    ship = Ship(ai_configuration, screen, statistics)
    return Bullet(ai_configuration, screen, ship)


def test_bullet_initialization(bullet: Bullet) -> None:
    """Test bullet initialization."""
    assert bullet.rect is not None
    assert bullet.screen is not None
    assert bullet.rect.width == 3  # Default bullet width from Configuration
    assert bullet.rect.height == 15  # Default bullet height from Configuration
    assert bullet.active is True


def test_bullet_movement(bullet: Bullet) -> None:
    """Test bullet movement."""
    initial_y = bullet.y
    bullet.update()
    assert bullet.y == initial_y - bullet.speed_factor


def test_bullet_deactivation(bullet: Bullet) -> None:
    """Test bullet deactivation when it goes off screen."""
    # Move bullet to just above the top of the screen
    bullet.y = -bullet.rect.height
    bullet.update()
    assert bullet.active is False
