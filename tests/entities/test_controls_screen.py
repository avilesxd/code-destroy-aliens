import pygame
import pytest

from src.config.configuration import Configuration
from src.config.language import Language
from src.entities.controls_screen import ControlsScreen


@pytest.fixture
def controls_screen() -> ControlsScreen:
    """Create a controls screen instance for testing."""
    pygame.init()
    screen = pygame.Surface((800, 600))
    config = Configuration()
    language = Language()
    return ControlsScreen(config, screen, language)


def test_controls_screen_initialization(controls_screen: ControlsScreen) -> None:
    """Test controls screen initialization."""
    assert controls_screen.screen is not None
    assert controls_screen.title is not None
    assert controls_screen.title_rect is not None
    assert controls_screen.title_rect.centerx == 400  # Screen width / 2
    assert controls_screen.title_rect.top == 50
    assert len(controls_screen.controls) == 4  # 4 control instructions
    assert controls_screen.continue_text is not None
    assert controls_screen.continue_rect is not None
    assert controls_screen.background is not None


def test_controls_screen_draw(controls_screen: ControlsScreen) -> None:
    """Test controls screen drawing."""
    # Draw the controls screen
    controls_screen.draw_controls()

    # Verify that all components are ready for drawing
    assert controls_screen.title is not None
    assert controls_screen.title_rect is not None
    assert controls_screen.controls is not None
    assert controls_screen.continue_text is not None
    assert controls_screen.continue_rect is not None
    assert controls_screen.background is not None


def test_controls_screen_text_positions(controls_screen: ControlsScreen) -> None:
    """Test controls screen text positions."""
    # Title should be at the top center
    assert controls_screen.title_rect.centerx == 400  # Screen width / 2
    assert controls_screen.title_rect.top == 50

    # Continue text should be near the bottom center
    assert controls_screen.continue_rect.centerx == 400  # Screen width / 2
    assert controls_screen.continue_rect.bottom == 550  # Screen height - 50
