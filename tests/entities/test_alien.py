import pygame
import pytest

from src.config.configuration import Configuration
from src.entities.alien import Alien


@pytest.fixture
def alien() -> Alien:
    """Create an alien instance for testing."""
    pygame.init()
    screen = pygame.Surface((800, 600))
    ai_configuration = Configuration()
    return Alien(ai_configuration, screen)


def test_alien_initialization(alien: Alien) -> None:
    """Test alien initialization."""
    assert alien.rect is not None
    assert alien.image is not None
    assert alien.screen is not None
    assert alien.ai_configuration is not None
    assert alien.music is not None
    assert alien.rect.width > 0
    assert alien.rect.height > 0


def test_alien_movement(alien: Alien) -> None:
    """Test alien movement."""
    initial_x = alien.x
    alien.update()
    speed_factor = alien.ai_configuration.alien_speed_factor
    fleet_direction = alien.ai_configuration.fleet_direction
    assert alien.x == initial_x + (speed_factor * fleet_direction)
    assert alien.rect.x == int(alien.x)


def test_alien_direction_change(alien: Alien) -> None:
    """Test alien direction change when hitting screen edge."""
    alien.rect.right = 800
    assert alien.check_edges() is True

    alien.rect.left = 0
    assert alien.check_edges() is True
