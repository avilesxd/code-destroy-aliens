import pygame
import pytest

from src.entities.heart import Heart


@pytest.fixture
def heart() -> Heart:
    """Create a heart instance for testing."""
    pygame.init()
    screen = pygame.Surface((800, 600))
    return Heart(screen)


def test_heart_initialization(heart: Heart) -> None:
    """Test heart initialization."""
    assert heart.image is not None
    assert heart.rect is not None
    assert heart.image.get_size() == (30, 30)


def test_heart_draw(heart: Heart) -> None:
    """Test heart drawing."""
    # This is a visual test, but we can verify the surface was created
    assert heart.image is not None
    assert heart.rect is not None
