"""Game logic module for Alien Invasion.

This module handles core game mechanics including:
- Alien movement and fleet management
- Bullet physics and collision detection
- Spatial grid optimization for efficient collision detection

The spatial grid system divides the game world into a grid of cells,
allowing for O(n) collision detection instead of O(n²) by only checking
objects in nearby cells.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple, TypedDict

import pygame

from src.config.actors.game_actors import check_aliens_bottom, create_fleet, ship_hit

if TYPE_CHECKING:
    from src.entities.alien import Alien
    from src.entities.bullet import Bullet
    from src.game import Game


class GridCell(TypedDict):
    """Type definition for spatial grid cell contents."""

    aliens: List[Alien]
    bullets: List[Bullet]


# Spatial Grid Configuration
# The spatial grid is a performance optimization technique that divides the game world
# into a grid of fixed-size cells. Each cell contains references to game objects
# (aliens and bullets) that occupy that space. This allows collision detection to only
# check objects in nearby cells instead of checking every object against every other object.
spatial_grid: Dict[Tuple[int, int], GridCell] = {}  # Maps (cell_x, cell_y) -> {"aliens": [...], "bullets": [...]}
grid_cell_size = 64  # Cell size in pixels - tuned for typical alien/bullet sizes


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


def get_grid_cells(rect: pygame.Rect) -> List[Tuple[int, int]]:
    """Calculates which grid cells a rectangle occupies in the spatial grid.

    The spatial grid divides the game world into a grid of fixed-size cells.
    A game object may occupy multiple cells if it spans across cell boundaries.

    For example, with a 64-pixel cell size:
    - A bullet at position (100, 200) occupies cell (1, 3)
    - An alien at position (120, 190) with width 40 might occupy cells (1, 2) and (1, 3)

    This function calculates all cells that a rectangle overlaps with.

    Args:
        rect (pygame.Rect): The rectangle to check (typically an alien or bullet rect)

    Returns:
        list: List of (cell_x, cell_y) tuples representing grid cell coordinates

    Algorithm:
        1. Calculate start cell: rect.left // cell_size, rect.top // cell_size
        2. Calculate end cell: rect.right // cell_size, rect.bottom // cell_size
        3. Return all cells in the range [start_x to end_x, start_y to end_y]
    """
    # Calculate the grid cell indices for the rectangle boundaries
    start_x = rect.left // grid_cell_size
    end_x = rect.right // grid_cell_size
    start_y = rect.top // grid_cell_size
    end_y = rect.bottom // grid_cell_size

    # Collect all cells that this rectangle overlaps
    cells: List[tuple[int, int]] = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            cells.append((x, y))
    return cells


def update_spatial_grid(game: Game) -> None:
    """Updates the spatial grid with current positions of aliens and bullets.

    The spatial grid optimization works by:
    1. Dividing the game world into a grid of 64x64 pixel cells
    2. Assigning each alien and bullet to the cell(s) they occupy
    3. Only checking collisions between objects in the same cell

    Performance benefit:
    - Without spatial grid: O(n * m) where n=bullets, m=aliens
    - With spatial grid: O(k) where k=average objects per cell
    - For typical gameplay: ~60x faster collision detection

    Example:
    - 100 bullets × 50 aliens = 5,000 collision checks (brute force)
    - With grid: ~10 objects per cell × 10 checks = 100 collision checks
    """
    global spatial_grid
    spatial_grid.clear()

    # Pre-allocate grid cells for better performance
    # Using a dictionary allows sparse grid (only populated cells exist)
    grid_cells: Dict[Tuple[int, int], GridCell] = {}

    # Phase 1: Add aliens to grid
    # Each alien is added to all cells it occupies (usually 1-4 cells)
    for alien in game.aliens:
        # Get all cells that the alien occupies
        alien_cells = get_grid_cells(alien.rect)
        for cell in alien_cells:
            if cell not in grid_cells:
                grid_cells[cell] = {"aliens": [], "bullets": []}
            grid_cells[cell]["aliens"].append(alien)

    # Phase 2: Add bullets to grid
    # Bullets are typically smaller and occupy fewer cells
    for bullet in game.bullets:
        # Get all cells that the bullet occupies
        bullet_cells = get_grid_cells(bullet.rect)
        for cell in bullet_cells:
            if cell not in grid_cells:
                grid_cells[cell] = {"aliens": [], "bullets": []}
            grid_cells[cell]["bullets"].append(bullet)

    # Phase 3: Update the global spatial grid
    # This replaces the old grid with the new one
    spatial_grid.update(grid_cells)


def check_bullet_alien_collisions(game: Game) -> None:
    """Responds to bullet-alien collisions using spatial grid optimization.

    Collision detection algorithm:
    1. Update spatial grid with current positions
    2. For each grid cell that contains both bullets AND aliens:
       - Only check collisions between objects in that cell
       - Mark bullet as inactive and remove alien on collision
       - Update score and trigger explosion effect
    3. Check for level completion (all aliens destroyed)
    4. Update high score if needed

    Why this is faster:
    - Brute force would check every bullet against every alien
    - Spatial grid only checks bullets against aliens in nearby cells
    - Most cells contain either bullets OR aliens, not both
    - Empty cells are skipped entirely
    """
    # Update spatial grid with current object positions
    update_spatial_grid(game)

    # Check collisions only in cells that contain both bullets and aliens
    # Most cells will have only one or the other, so this skips many cells
    for cell_data in spatial_grid.values():
        if cell_data["aliens"] and cell_data["bullets"]:
            # Check collisions between bullets and aliens in this cell only
            for bullet in cell_data["bullets"]:
                for alien in cell_data["aliens"]:
                    if bullet.rect.colliderect(alien.rect):
                        # Hit detected - deactivate bullet and destroy alien
                        bullet.active = False
                        alien.kill()
                        game.statistics.score += game.ai_configuration.alien_points
                        alien.explode()
                        game.scoreboard.prep_score()
                        break  # Bullet can only hit one alien

    check_high_score(game)

    # Check if all aliens are destroyed (level complete)
    if len(game.aliens) == 0:
        # Clear remaining bullets and start new level
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
