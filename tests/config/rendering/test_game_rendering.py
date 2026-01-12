import os
from unittest.mock import Mock, patch

import pygame

# Setting up headless mode for Pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from src.config.rendering.game_rendering import draw_fps_counter
from tests.conftest import MockGame


def test_draw_fps_counter(mock_game: MockGame) -> None:
    """Test if the FPS counter is drawn correctly."""
    # Enable FPS counter
    mock_game.ai_configuration.show_fps = True

    # Create a dummy surface for the FPS counter with a specific color
    fps_surface = pygame.Surface((100, 50))
    fps_color = (255, 0, 0)  # Red
    fps_surface.fill(fps_color)
    mock_game.fps_counter = fps_surface

    # Call the function to draw the FPS counter
    draw_fps_counter(mock_game)

    # Check the color of a pixel where the FPS counter should be
    pixel_x = mock_game.screen.get_width() - 50
    pixel_y = mock_game.screen.get_height() - 25
    pixel_color = mock_game.screen.get_at((pixel_x, pixel_y))

    # Assert that the color of the pixel is the same as the FPS counter color
    assert pixel_color == fps_color


def test_fps_counter_disabled(mock_game: MockGame) -> None:
    """Test that FPS counter is not drawn when disabled."""
    # Ensure FPS counter is disabled (default)
    mock_game.ai_configuration.show_fps = False

    # Create a dummy surface for the FPS counter
    fps_surface = pygame.Surface((100, 50))
    fps_surface.fill((255, 0, 0))  # Red
    mock_game.fps_counter = fps_surface

    # Store the background color
    bg_color = mock_game.screen.get_at((mock_game.screen.get_width() - 50, mock_game.screen.get_height() - 25))

    # Call the function to draw the FPS counter
    draw_fps_counter(mock_game)

    # Check that the pixel color hasn't changed (FPS counter not drawn)
    pixel_color = mock_game.screen.get_at((mock_game.screen.get_width() - 50, mock_game.screen.get_height() - 25))
    assert pixel_color == bg_color  # Should still be background color
