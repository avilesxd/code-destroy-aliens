from time import sleep

import pygame
from pygame.sprite import Group

from src.config.actors.fleet_calculations import get_number_aliens_x, get_number_rows
from src.config.configuration import Configuration
from src.config.statistics.statistics import Statistics
from src.entities.alien import Alien
from src.entities.scoreboard import Scoreboard
from src.entities.ship import Ship


def create_alien(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    aliens: Group,
    alien_number: int,
    row_number: int,
) -> None:
    """Creates a single alien and adds it to the aliens group.

    Args:
        ai_configuration (Settings): Game configuration settings
        screen (pygame.Surface): The game screen
        aliens (pygame.sprite.Group): Group of alien sprites
        alien_number (int): Position in the row (0-based)
        row_number (int): Row number (0-based)
    """
    alien = Alien(ai_configuration, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = int(alien.x)
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    ship: Ship,
    aliens: Group,
) -> None:
    """Creates a complete fleet of aliens arranged in rows and columns.

    Args:
        ai_configuration (Settings): Game configuration settings
        screen (pygame.Surface): The game screen
        ship (Ship): Player's ship
        aliens (pygame.sprite.Group): Group of alien sprites

    The fleet is created based on the available screen space and
    the dimensions of the ship and aliens.
    """
    # Create an alien and find the number of aliens in a row
    # The space between each alien is equal to one width of the alien
    alien = Alien(ai_configuration, screen)
    number_aliens_x = get_number_aliens_x(ai_configuration, alien.rect.width)
    number_rows = get_number_rows(ai_configuration, ship.rect.height, alien.rect.height)

    # Create the alien fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_configuration, screen, aliens, alien_number, row_number)


def ship_hit(
    ai_configuration: Configuration,
    statistics: Statistics,
    screen: pygame.Surface,
    scoreboard: Scoreboard,
    ship: Ship,
    aliens: Group,
    bullets: Group,
) -> None:
    """Responds to the ship being hit by an alien"""
    if statistics.ships_remaining > 0:
        # Decrements ships_remaining
        statistics.ships_remaining -= 1

        # Updates the scoreboard
        scoreboard.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_configuration, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        statistics.game_active = False
        statistics.end_game()  # This will play the game over sound
        pygame.mouse.set_visible(True)


def check_aliens_bottom(
    ai_configuration: Configuration,
    statistics: Statistics,
    screen: pygame.Surface,
    scoreboard: Scoreboard,
    ship: Ship,
    aliens: Group,
    bullets: Group,
) -> None:
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship were hit
            ship_hit(ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets)
            break
