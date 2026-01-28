"""Game actors module for Alien Invasion.

This module manages the creation and lifecycle of game entities:
- Alien fleet creation and positioning
- Ship collision handling and respawn logic
- Fleet edge detection and descent behavior
- Game state transitions (game over, level completion)

The factory pattern is used to create game entities, ensuring
consistent initialization and proper integration with the game state.
"""

from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

import pygame

from src.config.actors.fleet_calculations import get_number_aliens_x, get_number_rows
from src.entities.alien import Alien

if TYPE_CHECKING:
    from src.game import Game


def create_alien(game: Game, alien_number: int, row_number: int) -> None:
    """Creates a single alien and adds it to the aliens group."""
    alien = Alien(game.ai_configuration, game.screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = int(alien.x)
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    game.aliens.add(alien)


def create_fleet(game: Game) -> None:
    """Creates a complete fleet of aliens arranged in rows and columns."""
    alien = Alien(game.ai_configuration, game.screen)
    number_aliens_x = get_number_aliens_x(game.ai_configuration, alien.rect.width)
    number_rows = get_number_rows(game.ai_configuration, game.ship.rect.height, alien.rect.height)

    # Create the alien fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game, alien_number, row_number)


def ship_hit(game: Game) -> None:
    """Responds to the ship being hit by an alien"""
    if game.statistics.ships_remaining > 0:
        # Trigger strong rumble for ship hit
        game.gamepad.rumble(1.0, 1.0, 500)

        # Decrements ships_remaining
        game.statistics.ships_remaining -= 1

        # Updates the scoreboard
        game.scoreboard.prep_ships()

        # Empty the list of aliens and bullets
        game.aliens.empty()
        game.bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(game)
        game.ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        game.statistics.game_active = False
        game.statistics.end_game()  # This will play the game over sound
        pygame.mouse.set_visible(True)


def check_aliens_bottom(game: Game) -> None:
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = game.screen.get_rect()

    for alien in game.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship were hit
            ship_hit(game)
            break
