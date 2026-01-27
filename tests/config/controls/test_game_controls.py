import pygame
import pytest

from src.config.controls.game_controls import verify_events, verify_events_keydown, verify_events_keyup
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


def test_verify_events_keydown_move_left(mock_game: MockGame) -> None:
    """Test that the ship moves left when the left arrow key is pressed."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
    mock_game.ship.moving_left = False

    verify_events_keydown(event, mock_game)

    assert mock_game.ship.moving_left is True


def test_verify_events_keydown_space_close_controls(mock_game: MockGame) -> None:
    """Test that space key closes controls screen when shown."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    mock_game.statistics.show_controls = True
    mock_game.statistics.controls_seen = False

    verify_events_keydown(event, mock_game)

    assert mock_game.statistics.show_controls is False
    assert mock_game.statistics.controls_seen is True


def test_verify_events_keydown_space_fire_bullet(mock_game: MockGame) -> None:
    """Test that space key fires bullet when controls screen not shown."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    mock_game.statistics.show_controls = False
    initial_bullet_count = len(mock_game.bullets)

    verify_events_keydown(event, mock_game)

    # Verify a bullet was created
    assert len(mock_game.bullets) > initial_bullet_count


def test_verify_events_keydown_quit(mock_game: MockGame) -> None:
    """Test that Q key triggers exit."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)

    with pytest.raises(SystemExit):
        verify_events_keydown(event, mock_game)


def test_verify_events_keydown_pause(mock_game: MockGame) -> None:
    """Test that P key toggles pause state."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
    mock_game.statistics.game_paused = False

    verify_events_keydown(event, mock_game)

    assert mock_game.statistics.game_paused is True

    # Toggle again
    verify_events_keydown(event, mock_game)

    assert mock_game.statistics.game_paused is False


def test_verify_events_keydown_toggle_music(mock_game: MockGame) -> None:
    """Test that M key toggles music."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)

    # Just verify the function can be called without error
    verify_events_keydown(event, mock_game)


def test_verify_events_keydown_toggle_sound(mock_game: MockGame) -> None:
    """Test that S key toggles sound effects."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)
    initial_sound_state = mock_game.music.sound_effects_enabled

    verify_events_keydown(event, mock_game)

    assert mock_game.music.sound_effects_enabled != initial_sound_state


def test_verify_events_keyup_move_right(mock_game: MockGame) -> None:
    """Test that releasing right arrow stops ship movement."""
    event = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)
    mock_game.ship.moving_right = True

    verify_events_keyup(event, mock_game)

    assert mock_game.ship.moving_right is False


def test_verify_events_keyup_move_left(mock_game: MockGame) -> None:
    """Test that releasing left arrow stops ship movement."""
    event = pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT)
    mock_game.ship.moving_left = True

    verify_events_keyup(event, mock_game)

    assert mock_game.ship.moving_left is False


def test_verify_events_quit_event(mock_game: MockGame) -> None:
    """Test that QUIT event triggers exit."""
    # Post a QUIT event
    pygame.event.post(pygame.event.Event(pygame.QUIT))

    with pytest.raises(SystemExit):
        verify_events(mock_game)


def test_verify_events_keydown_integration(mock_game: MockGame) -> None:
    """Test that KEYDOWN events are processed correctly."""
    # Post a KEYDOWN event
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))

    mock_game.ship.moving_right = False
    verify_events(mock_game)

    assert mock_game.ship.moving_right is True


def test_verify_events_keyup_integration(mock_game: MockGame) -> None:
    """Test that KEYUP events are processed correctly."""
    # Post a KEYUP event
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))

    mock_game.ship.moving_right = True
    verify_events(mock_game)

    assert mock_game.ship.moving_right is False


def test_verify_events_mouse_button(mock_game: MockGame) -> None:
    """Test that mouse button events are processed."""
    # Set up game in inactive state with button visible
    mock_game.statistics.game_active = False
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 100)))

    # Should not raise an exception
    verify_events(mock_game)
