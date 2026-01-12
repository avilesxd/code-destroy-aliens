"""Game controls module for Alien Invasion.

This module handles all user input including:
- Keyboard controls for ship movement and shooting
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
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pygame

from src.config.rendering.game_rendering import check_play_button, fire_bullet

if TYPE_CHECKING:
    from src.game import Game


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
    elif event.key == pygame.K_p:
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


def verify_events_keyup(event: pygame.event.Event, game: Game) -> None:
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        game.ship.moving_left = False


def verify_events(game: Game) -> None:
    """Responds to keystrokes and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            verify_events_keydown(event, game)

        elif event.type == pygame.KEYUP:
            verify_events_keyup(event, game)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                game,
                mouse_x,
                mouse_y,
            )
