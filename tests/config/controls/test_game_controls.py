import pygame

from src.config.controls.game_controls import verify_events_keydown
from tests.conftest import MockGame


def test_verify_events_keydown_move_right(mock_game: MockGame) -> None:
    """Test that the ship moves right when the right arrow key is pressed."""
    # Create a mock event for the right arrow key press
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)

    # Ensure the ship is not moving right initially
    mock_game.ship.moving_right = False

    # Call the function to be tested
    verify_events_keydown(event, mock_game)

    # Assert that the ship is now moving right
    assert mock_game.ship.moving_right is True
