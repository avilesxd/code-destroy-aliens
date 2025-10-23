from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

import pygame

from src.config.actors.game_actors import check_aliens_bottom, create_fleet, ship_hit

if TYPE_CHECKING:
    from src.game import Game


# Global variables for spatial grid
spatial_grid: Dict[tuple, Dict[str, List]] = {}  # Dictionary to store objects in a spatial grid for collision detection
grid_cell_size = 64  # Size of each grid cell in pixels for spatial partitioning


def update_aliens(game: Game) -> None:
    """Checks if the fleet is at the edge and then updates the positions of all aliens in the fleet"""
    check_fleet_edges(game)
    game.aliens.update()

    # Check for alien-ship collisions
    if pygame.sprite.spritecollideany(game.ship, game.aliens):
        ship_hit(game)

    # Check for aliens hitting the bottom of the screen
    check_aliens_bottom(game)


def update_bullets(game: Game) -> None:
    """Updates the bullet positions and handles bullet-alien collisions."""
    # Updates the bullet positions
    game.bullets.update()

    # Remove inactive bullets from the group
    for bullet in game.bullets.copy():
        if not bullet.active:
            game.bullets.remove(bullet)

    check_bullet_alien_collisions(game)


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


def update_spatial_grid(game: Game) -> None:
    """Updates the spatial grid with current positions of aliens and bullets."""
    global spatial_grid
    spatial_grid.clear()

    # Pre-allocate grid cells for better performance
    grid_cells: Dict[tuple, Dict[str, List]] = {}

    # Add aliens to grid
    for alien in game.aliens:
        # Get all cells that the alien occupies
        alien_cells = get_grid_cells(alien.rect)
        for cell in alien_cells:
            if cell not in grid_cells:
                grid_cells[cell] = {"aliens": [], "bullets": []}
            grid_cells[cell]["aliens"].append(alien)

    # Add bullets to grid
    for bullet in game.bullets:
        # Get all cells that the bullet occupies
        bullet_cells = get_grid_cells(bullet.rect)
        for cell in bullet_cells:
            if cell not in grid_cells:
                grid_cells[cell] = {"aliens": [], "bullets": []}
            grid_cells[cell]["bullets"].append(bullet)

    # Update the global spatial grid
    spatial_grid.update(grid_cells)


def check_bullet_alien_collisions(game: Game) -> None:
    """Responds to bullet-alien collisions using spatial grid"""
    # Update spatial grid
    update_spatial_grid(game)

    # Check collisions only in cells that contain both bullets and aliens
    for cell_data in spatial_grid.values():
        if cell_data["aliens"] and cell_data["bullets"]:
            # Check collisions between bullets and aliens in this cell
            for bullet in cell_data["bullets"]:
                for alien in cell_data["aliens"]:
                    if bullet.rect.colliderect(alien.rect):
                        bullet.active = False
                        alien.kill()
                        game.statistics.score += game.ai_configuration.alien_points
                        alien.explode()
                        game.scoreboard.prep_score()
                        break

    check_high_score(game)

    if len(game.aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        game.bullets.empty()
        game.ai_configuration.boost_speed()
        game.statistics.level += 1
        game.scoreboard.prep_level()
        create_fleet(game)


def check_high_score(game: Game) -> None:
    """Checks if the current score is higher than the high score."""
    if game.statistics.score > game.statistics.high_score:
        game.statistics.high_score = game.statistics.score
        game.scoreboard.prep_high_score()
        game.statistics.save_high_score()  # Save the new high score


def check_fleet_edges(game: Game) -> None:
    """Respond appropriately if any alien has reached an edge"""
    for alien in game.aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game)
            break


def change_fleet_direction(game: Game) -> None:
    """Changes the direction of the alien fleet and moves it down."""
    for alien in game.aliens.sprites():
        alien.rect.y += game.ai_configuration.fleet_drop_speed
    game.ai_configuration.fleet_direction *= -1
