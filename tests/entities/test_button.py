import pygame
import pytest

from src.config.configuration import Configuration
from src.entities.button import Button


@pytest.fixture
def button() -> Button:
    """Create a button instance for testing."""
    pygame.init()
    screen = pygame.Surface((800, 600))
    config = Configuration()
    return Button(config, screen, "Test Button")


def test_button_initialization(button: Button) -> None:
    """Test button initialization."""
    assert button.rect.center == button.screen_rect.center
    assert button.width == 200
    assert button.height == 50
    assert button.button_color == (0, 255, 0)
    assert button.text_color == (255, 255, 255)


def test_button_prep_msg(button: Button) -> None:
    """Test button message preparation."""
    button.prep_msg("New Message")
    assert button.msg_image is not None
    assert button.msg_image_rect is not None
    assert button.msg_image_rect.center == button.rect.center


def test_button_draw(button: Button) -> None:
    """Test button drawing."""
    # This is a visual test, but we can verify the surfaces were created
    assert button.rect is not None
    assert button.msg_image is not None
    assert button.msg_image_rect is not None
