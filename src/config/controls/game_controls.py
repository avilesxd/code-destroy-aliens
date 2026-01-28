"""Game controls module for Alien Invasion.

This module handles all user input including:
- Keyboard controls for ship movement and shooting
- Gamepad/Joystick controls with haptic feedback
- Pause/resume game functionality
- Mouse input for button interactions
- Sound and music toggle controls

Key bindings:
- Arrow keys: Move ship left/right
- Space: Fire bullet / Close controls screen
- P: Pause/Resume game
- Q: Quit game
- S: Toggle sound effects
- M: Toggle background music

Gamepad bindings (Xbox layout):
- Left Stick / D-Pad: Move ship left/right
- A button: Fire bullet
- B button: Quit game
- Start: Pause/Resume game
- Back/Select: Show controls
- LB: Toggle sound effects
- RB: Toggle background music
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pygame

from src.config.controls.gamepad_controls import (
    verify_gamepad_axis,
    verify_gamepad_button_down,
    verify_gamepad_button_up,
    verify_gamepad_hat,
)
from src.config.rendering.game_rendering import check_play_button, fire_bullet

if TYPE_CHECKING:
    from src.game import Game


def _handle_game_controls(event: pygame.event.Event, game: Game) -> None:
    """Handle game control keys (pause, music, sound, gamepad config).

    Args:
        event: Pygame keyboard event
        game: Game object
    """
    if event.key == pygame.K_p:
        # Toggle pause state
        game.statistics.game_paused = not game.statistics.game_paused
        # Pause/resume music
        if game.statistics.game_paused:
            game.music.pause()
        else:
            game.music.resume()
    elif event.key == pygame.K_m:
        game.music.toggle_music()
    elif event.key == pygame.K_s:
        game.music.toggle_sound_effects()
    elif event.key == pygame.K_g:
        # Toggle gamepad configuration screen
        if game.gamepad.is_connected():
            game.statistics.show_gamepad_config = not game.statistics.show_gamepad_config


def verify_events_keydown(event: pygame.event.Event, game: Game) -> None:
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        game.ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if game.statistics.show_controls:
            game.statistics.show_controls = False
            game.statistics.controls_seen = True  # Mark controls as seen
        else:
            game.ship.shoot()
            fire_bullet(game)
    elif event.key == pygame.K_q:
        sys.exit()
    else:
        _handle_game_controls(event, game)


def verify_events_keyup(event: pygame.event.Event, game: Game) -> None:
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        game.ship.moving_left = False


def _handle_standard_events(event: pygame.event.Event, game: Game) -> None:
    """Handle standard keyboard/mouse events.

    Args:
        event: Pygame event
        game: Game object
    """
    if event.type == pygame.KEYDOWN:
        verify_events_keydown(event, game)
    elif event.type == pygame.KEYUP:
        verify_events_keyup(event, game)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        check_play_button(game, mouse_x, mouse_y)


def _handle_gamepad_events(event: pygame.event.Event, game: Game) -> None:
    """Handle gamepad-specific events.

    Args:
        event: Pygame event
        game: Game object
    """
    if event.type == pygame.JOYAXISMOTION:
        verify_gamepad_axis(event, game)
    elif event.type == pygame.JOYBUTTONDOWN:
        verify_gamepad_button_down(event, game)
    elif event.type == pygame.JOYBUTTONUP:
        verify_gamepad_button_up(event, game)
    elif event.type == pygame.JOYHATMOTION:
        verify_gamepad_hat(event, game)


def verify_events(game: Game) -> None:
    """Responds to keystrokes and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Handle gamepad config screen input separately
        if game.statistics.show_gamepad_config:
            # Handle keyboard input for gamepad config screen
            if game.gamepad_config_screen.handle_keyboard_input(event):
                game.statistics.show_gamepad_config = False
            # Handle gamepad button presses for remapping
            game.gamepad_config_screen.handle_gamepad_input(event)
            continue

        # Handle standard events (keyboard/mouse)
        _handle_standard_events(event, game)

        # Handle gamepad events
        _handle_gamepad_events(event, game)
