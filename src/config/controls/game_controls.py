import sys

import pygame
from pygame.sprite import Group

from src.config.configuration import Configuration
from src.config.music.music import Music
from src.config.rendering.game_rendering import check_play_button, fire_bullet
from src.config.statistics.statistics import Statistics
from src.entities.button import Button
from src.entities.scoreboard import Scoreboard
from src.entities.ship import Ship


def verify_events_keydown(
    event: pygame.event.Event,
    ai_configuration: Configuration,
    screen: pygame.Surface,
    ship: Ship,
    bullets: Group,
    statistics: Statistics,
    music: Music,
) -> None:
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if statistics.show_controls:
            statistics.show_controls = False
            statistics.controls_seen = True  # Mark controls as seen
        else:
            ship.shoot()
            fire_bullet(ai_configuration, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        # Toggle pause state
        statistics.game_paused = not statistics.game_paused
        # Pause/resume music
        if statistics.game_paused:
            music.pause()
        else:
            music.resume()
    elif event.key == pygame.K_m:
        music.toggle_music()
    elif event.key == pygame.K_s:
        music.toggle_sound_effects()


def verify_events_keyup(event: pygame.event.Event, ship: Ship) -> None:
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def verify_events(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    play_button: Button,
    ship: Ship,
    aliens: Group,
    bullets: Group,
    music: Music,
) -> None:
    """Responds to keystrokes and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            verify_events_keydown(
                event,
                ai_configuration,
                screen,
                ship,
                bullets,
                statistics,
                music,
            )

        elif event.type == pygame.KEYUP:
            verify_events_keyup(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_configuration,
                screen,
                statistics,
                scoreboard,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )
