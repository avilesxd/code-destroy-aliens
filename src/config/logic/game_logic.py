from typing import Dict, List

import pygame
from pygame.sprite import Group

from src.config.actors.game_actors import check_aliens_bottom, create_fleet, ship_hit
from src.config.configuration import Configuration
from src.config.statistics.statistics import Statistics
from src.entities.scoreboard import Scoreboard
from src.entities.ship import Ship

# Global variables for spatial grid
spatial_grid: Dict[tuple, Dict[str, List]] = {}  # Dictionary to store objects in a spatial grid for collision detection
grid_cell_size = 64  # Size of each grid cell in pixels for spatial partitioning


def update_aliens(
    ai_configuration: Configuration,
    statistics: Statistics,
    screen: pygame.Surface,
    scoreboard: Scoreboard,
    ship: Ship,
    aliens: Group,
    bullets: Group,
) -> None:
    """Checks if the fleet is at the edge and then updates the positions of all aliens in the fleet"""
    check_fleet_edges(ai_configuration, aliens)
    aliens.update()

    # Check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets)

    # Check for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets)


def update_bullets(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    ship: Ship,
    aliens: Group,
    bullets: Group,
) -> None:
    """Updates the bullet positions and handles bullet-alien collisions.

    Args:
        ai_configuration (Settings): Game configuration settings
        screen (pygame.Surface): The game screen
        statistics (Statistics): Game statistics object
        scoreboard (Scoreboard): Score display object
        ship (Ship): Player's ship
        aliens (pygame.sprite.Group): Group of alien sprites
        bullets (pygame.sprite.Group): Group of bullet sprites

    This function:
    1. Updates all bullet positions
    2. Removes inactive bullets
    3. Checks for bullet-alien collisions
    """
    # Updates the bullet positions
    bullets.update()

    # Remove inactive bullets from the group
    for bullet in bullets.sprites():
        if not bullet.active:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_configuration, screen, statistics, scoreboard, ship, aliens, bullets)


def get_grid_cells(rect: pygame.Rect) -> List[tuple[int, int]]:
    """Calculates which grid cells a rectangle occupies in the spatial grid.

    Args:
        rect (pygame.Rect): The rectangle to check

    Returns:
        list: List of (x, y) tuples representing grid cell coordinates

    The grid is used for spatial partitioning to optimize collision detection.
    """
    start_x = rect.left // grid_cell_size
    end_x = rect.right // grid_cell_size
    start_y = rect.top // grid_cell_size
    end_y = rect.bottom // grid_cell_size

    cells: List[tuple[int, int]] = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            cells.append((x, y))
    return cells


def update_spatial_grid(aliens: Group, bullets: Group) -> None:
    """Updates the spatial grid with current positions of aliens and bullets.

    Args:
        aliens (pygame.sprite.Group): Group of alien sprites
        bullets (pygame.sprite.Group): Group of bullet sprites

    This function rebuilds the spatial grid to reflect current object positions,
    which is used to optimize collision detection by only checking objects
    that are in the same grid cells.
    """
    global spatial_grid
    spatial_grid.clear()

    # Pre-allocate grid cells for better performance
    grid_cells: Dict[tuple, Dict[str, List]] = {}

    # Add aliens to grid
    for alien in aliens:
        # Get all cells that the alien occupies
        alien_cells = get_grid_cells(alien.rect)
        for cell in alien_cells:
            if cell not in grid_cells:
                grid_cells[cell] = {"aliens": [], "bullets": []}
            grid_cells[cell]["aliens"].append(alien)

    # Add bullets to grid
    for bullet in bullets:
        # Get all cells that the bullet occupies
        bullet_cells = get_grid_cells(bullet.rect)
        for cell in bullet_cells:
            if cell not in grid_cells:
                grid_cells[cell] = {"aliens": [], "bullets": []}
            grid_cells[cell]["bullets"].append(bullet)

    # Update the global spatial grid
    spatial_grid.update(grid_cells)


def check_bullet_alien_collisions(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    ship: Ship,
    aliens: Group,
    bullets: Group,
) -> None:
    """Responds to bullet-alien collisions using spatial grid"""
    # Update spatial grid
    update_spatial_grid(aliens, bullets)

    # Check collisions only in cells that contain both bullets and aliens
    for cell_data in spatial_grid.values():
        if cell_data["aliens"] and cell_data["bullets"]:
            # Check collisions between bullets and aliens in this cell
            for bullet in cell_data["bullets"]:
                for alien in cell_data["aliens"]:
                    if bullet.rect.colliderect(alien.rect):
                        bullet.active = False
                        alien.kill()
                        statistics.score += ai_configuration.alien_points
                        alien.explode()
                        scoreboard.prep_score()
                        break

    check_high_score(statistics, scoreboard)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_configuration.boost_speed()
        statistics.level += 1
        scoreboard.prep_level()
        create_fleet(ai_configuration, screen, ship, aliens)


def check_high_score(statistics: Statistics, scoreboard: Scoreboard) -> None:
    """Checks if the current score is higher than the high score.

    Args:
        statistics (Statistics): Game statistics object
        scoreboard (Scoreboard): Score display object

    If the current score is higher than the high score, updates the high score
    and saves it to persistent storage.
    """
    if statistics.score > statistics.high_score:
        statistics.high_score = statistics.score
        scoreboard.prep_high_score()
        statistics.save_high_score()  # Save the new high score


def check_fleet_edges(ai_configuration: Configuration, aliens: Group) -> None:
    """Respond appropriately if any alien has reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_configuration, aliens)
            break


def change_fleet_direction(ai_configuration: Configuration, aliens: Group) -> None:
    """Changes the direction of the alien fleet and moves it down.

    Args:
        ai_configuration (Settings): Game configuration settings
        aliens (pygame.sprite.Group): Group of alien sprites

    This function is called when the fleet hits the edge of the screen.
    It drops the fleet down and reverses its horizontal direction.
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_configuration.fleet_drop_speed
    ai_configuration.fleet_direction *= -1
