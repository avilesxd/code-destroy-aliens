import random
from typing import List, Optional, Tuple, Union

import pygame
from pygame.sprite import Group

from src.config.actors.game_actors import create_fleet
from src.config.configuration import Configuration
from src.config.statistics.statistics import Statistics
from src.entities.bullet import Bullet
from src.entities.button import Button
from src.entities.controls_screen import ControlsScreen
from src.entities.scoreboard import Scoreboard
from src.entities.ship import Ship

# Global variables for stars and gradient
stars: List[List[Union[int, float]]] = []  # List to store star positions and properties
last_star_time: int = 0  # Timestamp of the last star creation
cached_gradient: Optional[pygame.Surface] = None  # Cached gradient surface to avoid recreation
last_screen_size: Optional[Tuple[int, int]] = None  # Last screen dimensions used for gradient


def create_gradient_surface(screen: pygame.Surface, top_color: tuple, bottom_color: tuple) -> pygame.Surface:
    """Creates a surface with a vertical gradient from top_color to bottom_color.

    Args:
        screen (pygame.Surface): The screen surface to get dimensions from
        top_color (tuple): RGB color tuple for the top of the gradient
        bottom_color (tuple): RGB color tuple for the bottom of the gradient

    Returns:
        pygame.Surface: A surface with the gradient applied

    Note:
        This function caches the gradient surface to improve performance
        when the screen size hasn't changed.
    """
    global cached_gradient, last_screen_size

    # Check if we can reuse the cached gradient
    current_size = (screen.get_width(), screen.get_height())

    if cached_gradient and last_screen_size == current_size:
        return cached_gradient

    # Create new gradient if needed
    gradient = pygame.Surface(current_size)
    for y in range(current_size[1]):
        ratio = y / current_size[1]
        color = [int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio) for i in range(3)]
        pygame.draw.line(gradient, color, (0, y), (current_size[0], y))

    # Cache the gradient
    cached_gradient = gradient
    last_screen_size = current_size

    return gradient


def update_stars(
    screen: pygame.Surface,
    ai_configuration: Configuration,
    is_paused: bool = False,
    is_game_over: bool = False,
) -> None:
    """Updates and draws the stars"""
    global stars, last_star_time

    # Create initial stars if they don't exist
    if not stars:
        for _ in range(ai_configuration.star_count):
            x = random.randint(0, ai_configuration.screen_width)
            y = random.randint(0, ai_configuration.screen_height)
            size = random.randint(1, 3)
            speed = random.uniform(0.1, 0.5)
            stars.append([x, y, size, speed])

    # Update star positions only if enough time has passed and game is not paused
    if not is_paused and not is_game_over:
        for star in stars:
            star[1] += star[3]  # Move the star downward
            if star[1] > ai_configuration.screen_height:
                star[1] = 0
                star[0] = random.randint(0, ai_configuration.screen_width)

    # Draw the stars
    for star_x, star_y, star_size, _ in stars:
        x_int: int = int(star_x)
        y_int: int = int(star_y)
        size_int: int = int(star_size)
        pygame.draw.circle(screen, ai_configuration.star_color, (x_int, y_int), size_int)


def check_play_button(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    play_button: Button,
    ship: Ship,
    aliens: Group,
    bullets: Group,
    mouse_x: int,
    mouse_y: int,
) -> None:
    """Starts a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not statistics.game_active:
        # Resets the game configuration
        ai_configuration.initialize_dynamic_configurations()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Resets the game statistics
        statistics.reset_stats()
        statistics.game_active = True
        statistics.game_paused = False  # Reset pause state

        # Resets the scoreboard images
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_configuration, screen, ship, aliens)
        ship.center_ship()


def update_screen(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    ship: Ship,
    aliens: Group,
    bullets: Group,
    play_button: Button,
    controls_screen: ControlsScreen,
) -> None:
    """Updates the images on the screen and switches to the new screen"""

    if ai_configuration.use_gradient_background:
        # Create and draw the gradient
        gradient = create_gradient_surface(
            screen,
            ai_configuration.gradient_top_color,
            ai_configuration.gradient_bottom_color,
        )
        screen.blit(gradient, (0, 0))

        # Update and draw stars if they are enabled
        if ai_configuration.use_stars:
            update_stars(screen, ai_configuration, statistics.game_paused, statistics.game_over)
    else:
        # Use solid background color if gradient is disabled
        screen.fill(ai_configuration.bg_color)

    # Redraws all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    scoreboard.show_score()

    # Draw the controls screen if it's active
    if statistics.show_controls:
        controls_screen.draw_controls()
    # Draw the Play button if the game is inactive and controls are not showing
    elif not statistics.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def fire_bullet(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    ship: Ship,
    bullets: Group,
) -> None:
    """Creates and fires a new bullet if the bullet limit hasn't been reached.

    Args:
        ai_configuration (Settings): Game configuration settings
        screen (pygame.Surface): The game screen
        ship (Ship): Player's ship
        bullets (pygame.sprite.Group): Group of bullet sprites
    """
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_configuration.bullets_allowed:
        new_bullet = Bullet.get_bullet(ai_configuration, screen, ship)
        bullets.add(new_bullet)
