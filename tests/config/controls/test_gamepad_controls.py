"""Tests for gamepad controls functionality."""

from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pygame
import pytest

from src.config.controls.gamepad_controls import (
    GamepadManager,
    verify_gamepad_axis,
    verify_gamepad_button_down,
    verify_gamepad_button_up,
    verify_gamepad_hat,
)


class TestGamepadManager:
    """Test suite for GamepadManager class."""

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_init_with_gamepad_connected(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test GamepadManager initialization when gamepad is connected."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Xbox Controller"
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True)

        assert manager.enabled is True
        assert manager.joystick is not None
        mock_joystick.init.assert_called_once()

    @patch("pygame.joystick.get_count")
    def test_init_with_no_gamepad(self, mock_get_count: Any) -> None:
        """Test GamepadManager initialization when no gamepad is connected."""
        mock_get_count.return_value = 0  # type: ignore[unreachable]

        manager = GamepadManager(enabled=True)

        assert manager.enabled is True
        assert manager.joystick is None

    def test_init_disabled(self) -> None:
        """Test GamepadManager initialization when disabled."""
        manager = GamepadManager(enabled=False)

        assert manager.enabled is False
        assert manager.joystick is None

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_is_connected_true(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test is_connected returns True when gamepad is connected."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Test Controller"
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True)

        assert manager.is_connected() is True

    def test_is_connected_false_no_joystick(self) -> None:
        """Test is_connected returns False when no gamepad."""
        manager = GamepadManager(enabled=False)

        assert manager.is_connected() is False

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_get_axis_value_with_deadzone(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test get_axis_value applies deadzone correctly."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Test Controller"
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True, deadzone=0.15)

        # Value below deadzone should return 0.0
        mock_joystick.get_axis.return_value = 0.1
        assert manager.get_axis_value(0) == 0.0

        # Value above deadzone should return actual value
        mock_joystick.get_axis.return_value = 0.5
        assert manager.get_axis_value(0) == 0.5

        # Negative value below deadzone should return 0.0
        mock_joystick.get_axis.return_value = -0.1
        assert manager.get_axis_value(0) == 0.0

        # Negative value above deadzone should return actual value
        mock_joystick.get_axis.return_value = -0.5
        assert manager.get_axis_value(0) == -0.5

    def test_get_axis_value_no_gamepad(self) -> None:
        """Test get_axis_value returns 0.0 when no gamepad."""
        manager = GamepadManager(enabled=False)

        assert manager.get_axis_value(0) == 0.0

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_get_button(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test get_button returns button state."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Test Controller"
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True)

        # Button pressed
        mock_joystick.get_button.return_value = True
        assert manager.get_button(0) is True

        # Button not pressed
        mock_joystick.get_button.return_value = False
        assert manager.get_button(0) is False

    def test_get_button_no_gamepad(self) -> None:
        """Test get_button returns False when no gamepad."""
        manager = GamepadManager(enabled=False)

        assert manager.get_button(0) is False

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_get_hat(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test get_hat returns D-Pad state."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Test Controller"
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True)

        # D-Pad left
        mock_joystick.get_hat.return_value = (-1, 0)
        assert manager.get_hat(0) == (-1, 0)

        # D-Pad right
        mock_joystick.get_hat.return_value = (1, 0)
        assert manager.get_hat(0) == (1, 0)

    def test_get_hat_no_gamepad(self) -> None:
        """Test get_hat returns (0, 0) when no gamepad."""
        manager = GamepadManager(enabled=False)

        assert manager.get_hat(0) == (0, 0)

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_rumble_with_support(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test rumble triggers haptic feedback when supported."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Xbox Controller"
        mock_joystick.rumble = Mock()
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True)
        manager.rumble_support = True

        manager.rumble(0.5, 1.0, 200)

        mock_joystick.rumble.assert_called_once_with(0.5, 1.0, 200)

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_rumble_without_support(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test rumble does nothing when not supported."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Generic Controller"
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True)
        manager.rumble_support = False

        # Should not raise exception
        manager.rumble(0.5, 1.0, 200)

    @patch("pygame.joystick.get_count")
    @patch("pygame.joystick.Joystick")
    def test_stop_rumble(self, mock_joystick_class: Any, mock_get_count: Any) -> None:
        """Test stop_rumble stops haptic feedback."""
        mock_get_count.return_value = 1
        mock_joystick = Mock()
        mock_joystick.get_name.return_value = "Xbox Controller"
        mock_joystick.stop_rumble = Mock()
        mock_joystick_class.return_value = mock_joystick

        manager = GamepadManager(enabled=True)
        manager.rumble_support = True

        manager.stop_rumble()

        mock_joystick.stop_rumble.assert_called_once()


class TestGamepadEvents:
    """Test suite for gamepad event handlers."""

    def test_verify_gamepad_axis_left_movement(self, mock_game: Any) -> None:
        """Test left stick moves ship left."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.get_axis_value.return_value = -0.8  # Left
        mock_game.gamepad.deadzone = 0.15

        event = Mock()
        event.axis = 0  # Left stick horizontal

        verify_gamepad_axis(event, mock_game)

        assert mock_game.ship.moving_left is True
        assert mock_game.ship.moving_right is False

    def test_verify_gamepad_axis_right_movement(self, mock_game: Any) -> None:
        """Test left stick moves ship right."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.get_axis_value.return_value = 0.8  # Right
        mock_game.gamepad.deadzone = 0.15

        event = Mock()
        event.axis = 0  # Left stick horizontal

        verify_gamepad_axis(event, mock_game)

        assert mock_game.ship.moving_right is True
        assert mock_game.ship.moving_left is False

    def test_verify_gamepad_axis_centered(self, mock_game: Any) -> None:
        """Test centered stick stops ship movement."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.get_axis_value.return_value = 0.0  # Centered
        mock_game.gamepad.deadzone = 0.15

        event = Mock()
        event.axis = 0

        verify_gamepad_axis(event, mock_game)

        assert mock_game.ship.moving_left is False
        assert mock_game.ship.moving_right is False

    def test_verify_gamepad_axis_not_connected(self, mock_game: Any) -> None:
        """Test axis event does nothing when gamepad not connected."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = False

        event = Mock()
        event.axis = 0

        # Should not raise exception
        verify_gamepad_axis(event, mock_game)

    @patch("src.config.controls.gamepad_controls.fire_bullet")
    def test_verify_gamepad_button_fire(self, mock_fire_bullet: Any, mock_game: Any) -> None:
        """Test A button fires bullet."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.rumble = Mock()
        mock_game.gamepad.config = Mock()
        mock_game.gamepad.config.get_action_for_button.return_value = "fire"
        mock_game.statistics.show_controls = False
        mock_game.ship.shoot = Mock()

        event = Mock()
        event.button = 0  # A button

        verify_gamepad_button_down(event, mock_game)

        mock_game.ship.shoot.assert_called_once()
        mock_fire_bullet.assert_called_once_with(mock_game)
        mock_game.gamepad.rumble.assert_called_once()

    def test_verify_gamepad_button_close_controls(self, mock_game: Any) -> None:
        """Test A button closes controls screen."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.config = Mock()
        mock_game.gamepad.config.get_action_for_button.return_value = "fire"
        mock_game.statistics.show_controls = True

        event = Mock()
        event.button = 0  # A button

        verify_gamepad_button_down(event, mock_game)

        assert mock_game.statistics.show_controls is False
        assert mock_game.statistics.controls_seen is True

    def test_verify_gamepad_button_pause(self, mock_game: Any) -> None:
        """Test Start button pauses game."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.config = Mock()
        mock_game.gamepad.config.get_action_for_button.return_value = "pause"
        mock_game.statistics.game_paused = False
        mock_game.music = Mock()

        event = Mock()
        event.button = 7  # Start button

        verify_gamepad_button_down(event, mock_game)

        assert mock_game.statistics.game_paused is True
        mock_game.music.pause.assert_called_once()

    def test_verify_gamepad_button_resume(self, mock_game: Any) -> None:
        """Test Start button resumes game."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.config = Mock()
        mock_game.gamepad.config.get_action_for_button.return_value = "pause"
        mock_game.statistics.game_paused = True
        mock_game.music = Mock()

        event = Mock()
        event.button = 7  # Start button

        verify_gamepad_button_down(event, mock_game)

        assert mock_game.statistics.game_paused is False
        mock_game.music.resume.assert_called_once()

    def test_verify_gamepad_button_toggle_sound(self, mock_game: Any) -> None:
        """Test LB toggles sound effects."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.config = Mock()
        mock_game.gamepad.config.get_action_for_button.return_value = "toggle_sound"
        mock_game.music = Mock()

        event = Mock()
        event.button = 4  # LB

        verify_gamepad_button_down(event, mock_game)

        mock_game.music.toggle_sound_effects.assert_called_once()

    def test_verify_gamepad_button_toggle_music(self, mock_game: Any) -> None:
        """Test RB toggles background music."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.config = Mock()
        mock_game.gamepad.config.get_action_for_button.return_value = "toggle_music"
        mock_game.music = Mock()

        event = Mock()
        event.button = 5  # RB

        verify_gamepad_button_down(event, mock_game)

        mock_game.music.toggle_music.assert_called_once()

    def test_verify_gamepad_hat_left(self, mock_game: Any) -> None:
        """Test D-Pad left moves ship left."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.get_hat.return_value = (-1, 0)

        event = Mock()

        verify_gamepad_hat(event, mock_game)

        assert mock_game.ship.moving_left is True
        assert mock_game.ship.moving_right is False

    def test_verify_gamepad_hat_right(self, mock_game: Any) -> None:
        """Test D-Pad right moves ship right."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.get_hat.return_value = (1, 0)

        event = Mock()

        verify_gamepad_hat(event, mock_game)

        assert mock_game.ship.moving_right is True
        assert mock_game.ship.moving_left is False

    def test_verify_gamepad_hat_centered(self, mock_game: Any) -> None:
        """Test centered D-Pad stops ship movement."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True
        mock_game.gamepad.get_hat.return_value = (0, 0)

        event = Mock()

        verify_gamepad_hat(event, mock_game)

        assert mock_game.ship.moving_left is False
        assert mock_game.ship.moving_right is False

    def test_verify_gamepad_button_up(self, mock_game: Any) -> None:
        """Test button release handler exists."""
        mock_game.gamepad = Mock()
        mock_game.gamepad.is_connected.return_value = True

        event = Mock()
        event.button = 0

        # Should not raise exception
        verify_gamepad_button_up(event, mock_game)
