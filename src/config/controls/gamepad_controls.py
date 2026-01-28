"""Gamepad/Joystick controls module.

This module handles all gamepad input including:
- Automatic detection of connected gamepads
- Support for Xbox, PlayStation, and generic controllers
- Analog stick movement with configurable dead zones
- Button mapping for all game actions
- Haptic feedback (rumble) for collisions and shooting

Controller mapping (Xbox layout as reference):
- Left Stick / D-Pad: Move ship left/right
- A button (button 0): Fire bullet
- Start button (button 7): Pause/Resume game
- Back/Select button (button 6): Show controls
- LB (button 4): Toggle sound effects
- RB (button 5): Toggle background music
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Optional

import pygame

from src.config.controls.gamepad_config import GamepadConfig
from src.config.rendering.game_rendering import fire_bullet

if TYPE_CHECKING:
    from src.game import Game


class GamepadManager:
    """Manages gamepad detection, input, and haptic feedback.

    Attributes:
        joystick (Optional[Any]): The active gamepad
        enabled (bool): Whether gamepad support is enabled
        deadzone (float): Minimum axis value to register input (prevents drift)
        rumble_support (bool): Whether the gamepad supports haptic feedback
    """

    def __init__(self, enabled: bool = True, deadzone: float = 0.15, preset: str = "xbox") -> None:
        """Initialize the gamepad manager.

        Args:
            enabled: Whether to enable gamepad support
            deadzone: Minimum axis value to register input (0.0-1.0)
            preset: Controller preset to load (xbox, playstation, nintendo)
        """
        self.joystick: Optional[object] = None
        self.enabled = enabled
        self.deadzone = deadzone
        self.rumble_support = False
        self.config = GamepadConfig(preset=preset)

        if self.enabled:
            self._init_gamepad()

    def _init_gamepad(self) -> None:
        """Initialize the first available gamepad."""
        pygame.joystick.init()

        # Check if any joysticks are connected
        joystick_count = pygame.joystick.get_count()

        if joystick_count > 0:
            # Initialize the first joystick
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

            # Check for rumble support (haptic feedback)
            try:
                # Try to use rumble - if it works, we have support
                if hasattr(self.joystick, "rumble"):
                    self.rumble_support = True
                    print(f"✓ Gamepad detected: {self.joystick.get_name()}")
                    print("✓ Rumble support: Yes")
                else:
                    self.rumble_support = False
                    print(f"✓ Gamepad detected: {self.joystick.get_name()}")
                    print("✓ Rumble support: No")
            except Exception:
                self.rumble_support = False
        else:
            print("○ No gamepad detected - using keyboard only")

    def is_connected(self) -> bool:
        """Check if a gamepad is currently connected.

        Returns:
            True if gamepad is connected and enabled, False otherwise
        """
        return self.enabled and self.joystick is not None

    def rumble(self, low_frequency: float = 0.0, high_frequency: float = 1.0, duration: int = 100) -> None:
        """Trigger haptic feedback on the gamepad.

        Args:
            low_frequency: Low frequency rumble intensity (0.0-1.0)
            high_frequency: High frequency rumble intensity (0.0-1.0)
            duration: Duration of rumble in milliseconds
        """
        if self.rumble_support and self.joystick:
            try:
                self.joystick.rumble(low_frequency, high_frequency, duration)  # type: ignore[attr-defined]
            except Exception:
                # Silently fail if rumble doesn't work
                pass

    def stop_rumble(self) -> None:
        """Stop any ongoing rumble effect."""
        if self.rumble_support and self.joystick:
            try:
                self.joystick.stop_rumble()  # type: ignore[attr-defined]
            except Exception:
                pass

    def get_axis_value(self, axis: int) -> float:
        """Get the value of a joystick axis with deadzone applied.

        Args:
            axis: Axis index to read

        Returns:
            Axis value (-1.0 to 1.0) with deadzone applied, or 0.0 if not connected
        """
        if not self.is_connected() or not self.joystick:
            return 0.0

        try:
            value = self.joystick.get_axis(axis)  # type: ignore[attr-defined]
            # Apply deadzone
            if abs(value) < self.deadzone:
                return 0.0
            return float(value)
        except Exception:
            return 0.0

    def get_button(self, button: int) -> bool:
        """Get the state of a gamepad button.

        Args:
            button: Button index to check

        Returns:
            True if button is pressed, False otherwise
        """
        if not self.is_connected() or not self.joystick:
            return False

        try:
            return bool(self.joystick.get_button(button))  # type: ignore[attr-defined]
        except Exception:
            return False

    def get_hat(self, hat: int) -> tuple[int, int]:
        """Get the state of a D-Pad (hat).

        Args:
            hat: Hat index (usually 0 for D-Pad)

        Returns:
            Tuple of (x, y) values: (-1, 0, 1) for each axis
        """
        if not self.is_connected() or not self.joystick:
            return (0, 0)

        try:
            hat_value = self.joystick.get_hat(hat)  # type: ignore[attr-defined]
            return (int(hat_value[0]), int(hat_value[1]))
        except Exception:
            return (0, 0)


def verify_gamepad_axis(event: pygame.event.Event, game: Game) -> None:
    """Handle analog stick movement.

    Axis mapping (common for most controllers):
    - Axis 0: Left stick horizontal (-1=left, 1=right)
    - Axis 1: Left stick vertical (-1=up, 1=down)
    - Axis 2: Right stick horizontal
    - Axis 3: Right stick vertical

    Args:
        event: Pygame JOYAXISMOTION event
        game: Game object containing ship and configuration
    """
    if not game.gamepad.is_connected():
        return

    # Left stick horizontal (Axis 0) - ship movement
    if event.axis == 0:
        value = game.gamepad.get_axis_value(0)

        if value < -game.gamepad.deadzone:
            # Moving left
            game.ship.moving_left = True
            game.ship.moving_right = False
        elif value > game.gamepad.deadzone:
            # Moving right
            game.ship.moving_right = True
            game.ship.moving_left = False
        else:
            # Centered - stop movement
            game.ship.moving_left = False
            game.ship.moving_right = False


def _handle_action_button(game: Game) -> None:
    """Handle A button press (fire bullet or close controls).

    Args:
        game: Game object
    """
    if game.statistics.show_controls:
        game.statistics.show_controls = False
        game.statistics.controls_seen = True
    else:
        game.ship.shoot()
        fire_bullet(game)
        # Light rumble when shooting
        game.gamepad.rumble(0.0, 0.3, 50)


def _handle_pause_button(game: Game) -> None:
    """Handle Start button press (pause/resume game).

    Args:
        game: Game object
    """
    game.statistics.game_paused = not game.statistics.game_paused
    if game.statistics.game_paused:
        game.music.pause()
    else:
        game.music.resume()


def verify_gamepad_button_down(event: pygame.event.Event, game: Game) -> None:
    """Handle gamepad button press events using custom button mapping.

    Uses the GamepadConfig to determine which action each button performs.
    This allows users to customize their controller layout.

    Args:
        event: Pygame JOYBUTTONDOWN event
        game: Game object
    """
    if not game.gamepad.is_connected():
        return

    # Get the action mapped to this button
    action = game.gamepad.config.get_action_for_button(event.button)

    if action == "fire":
        _handle_action_button(game)
    elif action == "quit":
        sys.exit()
    elif action == "toggle_sound":
        game.music.toggle_sound_effects()
    elif action == "toggle_music":
        game.music.toggle_music()
    elif action == "show_controls":
        if not game.statistics.show_controls:
            game.statistics.show_controls = True
    elif action == "pause":
        _handle_pause_button(game)


def verify_gamepad_button_up(event: pygame.event.Event, game: Game) -> None:
    """Handle gamepad button release events.

    Currently, most game actions are handled on button press.
    This function is here for potential future use.

    Args:
        event: Pygame JOYBUTTONUP event
        game: Game object
    """
    # Reserved for future use
    pass


def verify_gamepad_hat(event: pygame.event.Event, game: Game) -> None:
    """Handle D-Pad input for ship movement.

    The D-Pad (hat) provides digital directional input as an alternative
    to the analog stick.

    Hat values:
    - (0, 0): Centered
    - (-1, 0): Left
    - (1, 0): Right
    - (0, -1): Down
    - (0, 1): Up

    Args:
        event: Pygame JOYHATMOTION event
        game: Game object
    """
    if not game.gamepad.is_connected():
        return

    hat_x, hat_y = game.gamepad.get_hat(0)

    # Update ship movement based on D-Pad
    if hat_x < 0:
        # D-Pad left
        game.ship.moving_left = True
        game.ship.moving_right = False
    elif hat_x > 0:
        # D-Pad right
        game.ship.moving_right = True
        game.ship.moving_left = False
    else:
        # D-Pad centered horizontally
        game.ship.moving_left = False
        game.ship.moving_right = False
