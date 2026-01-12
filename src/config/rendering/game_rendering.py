"""Game rendering module for Alien Invasion.

This module handles all visual rendering including:
- Screen updates and background rendering
- Gradient backgrounds with star field effects
- FPS counter display
- Game entity rendering coordination

Performance optimizations:
- Gradient surface caching to avoid regenerating each frame
- Star field animation with minimal overhead
- Conditional FPS counter rendering
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

import pygame

from src.config.actors.game_actors import create_fleet
from src.entities.bullet import Bullet

if TYPE_CHECKING:
    from src.game import Game


# Rendering state and caching
stars: List[List[Union[int, float]]] = []  # Star positions: [[x, y, brightness], ...]
last_star_time: int = 0  # Timestamp for star creation rate limiting
cached_gradient: Optional[pygame.Surface] = None  # Cached gradient to avoid recreation
last_screen_size: Optional[Tuple[int, int]] = None  # Last screen size for cache invalidation


def create_gradient_surface(screen: pygame.Surface, top_color: tuple, bottom_color: tuple) -> pygame.Surface:
    """Creates a surface with a vertical gradient from top_color to bottom_color."""
    global cached_gradient, last_screen_size

    current_size = (screen.get_width(), screen.get_height())

    if cached_gradient and last_screen_size == current_size:
        return cached_gradient

    gradient = pygame.Surface(current_size)
    for y in range(current_size[1]):
        ratio = y / current_size[1]
        color = [int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio) for i in range(3)]
        pygame.draw.line(gradient, color, (0, y), (current_size[0], y))

    cached_gradient = gradient
    last_screen_size = current_size

    return gradient


def update_stars(game: Game) -> None:
    """Updates and draws the stars"""
    global stars

    if not stars:
        for _ in range(game.ai_configuration.star_count):
            x = random.randint(0, game.ai_configuration.screen_width)
            y = random.randint(0, game.ai_configuration.screen_height)
            size = random.randint(1, 3)
            speed = random.uniform(0.1, 0.5)
            stars.append([x, y, size, speed])

    if not game.statistics.game_paused and not game.statistics.game_over:
        for star in stars:
            star[1] += star[3]  # Move the star downward
            if star[1] > game.ai_configuration.screen_height:
                star[1] = 0
                star[0] = random.randint(0, game.ai_configuration.screen_width)

    for star_x, star_y, star_size, _ in stars:
        x_int: int = int(star_x)
        y_int: int = int(star_y)
        size_int: int = int(star_size)
        pygame.draw.circle(game.screen, game.ai_configuration.star_color, (x_int, y_int), size_int)


def check_play_button(
    game: Game,
    mouse_x: int,
    mouse_y: int,
) -> None:
    """Starts a new game when the player clicks Play"""
    button_clicked = game.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not game.statistics.game_active:
        game.ai_configuration.initialize_dynamic_configurations()
        pygame.mouse.set_visible(False)
        game.statistics.reset_stats()
        game.statistics.game_active = True
        game.statistics.game_paused = False
        game.scoreboard.prep_score()
        game.scoreboard.prep_high_score()
        game.scoreboard.prep_level()
        game.scoreboard.prep_ships()
        game.aliens.empty()
        game.bullets.empty()
        create_fleet(game)
        game.ship.center_ship()


def draw_fps_counter(game: Game) -> None:
    """Draws the FPS counter on the screen if enabled."""
    if game.ai_configuration.show_fps and game.fps_counter:
        game.screen.blit(
            game.fps_counter,
            (
                game.screen.get_width() - game.fps_counter.get_width() - 10,
                game.screen.get_height() - game.fps_counter.get_height() - 10,
            ),
        )


def update_screen(game: Game) -> None:
    """Updates the images on the screen and switches to the new screen"""
    if game.ai_configuration.use_gradient_background:
        gradient = create_gradient_surface(
            game.screen,
            game.ai_configuration.gradient_top_color,
            game.ai_configuration.gradient_bottom_color,
        )
        game.screen.blit(gradient, (0, 0))
        if game.ai_configuration.use_stars:
            update_stars(game)
    else:
        game.screen.fill(game.ai_configuration.bg_color)

    for bullet in game.bullets.sprites():
        bullet.draw_bullet()
    game.ship.blitme()
    game.aliens.draw(game.screen)

    game.scoreboard.show_score()

    if game.statistics.show_controls:
        game.controls_screen.draw_controls()
    elif not game.statistics.game_active:
        game.play_button.draw_button()

    draw_fps_counter(game)

    pygame.display.flip()


def fire_bullet(game: Game) -> None:
    """Creates and fires a new bullet if the bullet limit hasn't been reached."""
    if len(game.bullets) < game.ai_configuration.bullets_allowed:
        new_bullet = Bullet.get_bullet(game.ai_configuration, game.screen, game.ship)
        game.bullets.add(new_bullet)
