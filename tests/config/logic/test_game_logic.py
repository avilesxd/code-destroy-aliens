"""Tests for game logic module."""

import pygame
from pygame.sprite import Group

from src.config.actors.game_actors import create_alien, create_fleet
from src.config.logic.game_logic import (
    change_fleet_direction,
    check_bullet_alien_collisions,
    check_fleet_edges,
    check_high_score,
    get_grid_cells,
    spatial_grid,
    update_aliens,
    update_bullets,
    update_spatial_grid,
)
from src.entities.bullet import Bullet
from tests.conftest import MockGame


def test_update_aliens(mock_game: MockGame) -> None:
    """Test that update_aliens moves aliens."""
    create_alien(mock_game, alien_number=0, row_number=0)
    alien = list(mock_game.aliens.sprites())[0]
    initial_x = alien.x

    update_aliens(mock_game)

    # Alien should have moved
    assert alien.x != initial_x


def test_update_aliens_ship_collision(mock_game: MockGame) -> None:
    """Test that alien-ship collision triggers ship_hit."""
    mock_game.aliens.empty()
    create_alien(mock_game, alien_number=0, row_number=0)
    alien = list(mock_game.aliens.sprites())[0]

    # Move alien to ship position for collision
    alien.rect.centerx = mock_game.ship.rect.centerx
    alien.rect.centery = mock_game.ship.rect.centery
    initial_ships = mock_game.statistics.ships_remaining

    update_aliens(mock_game)

    # Ship should have been hit - ship_hit creates new fleet
    # So check that ships decreased (or game is over)
    assert mock_game.statistics.ships_remaining < initial_ships or mock_game.statistics.game_active is False


def test_update_bullets(mock_game: MockGame) -> None:
    """Test that update_bullets moves bullets."""
    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)
    initial_y = bullet.y

    update_bullets(mock_game)

    # Bullet should have moved up
    assert bullet.y < initial_y


def test_update_bullets_removes_inactive(mock_game: MockGame) -> None:
    """Test that inactive bullets are removed."""
    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)
    bullet.active = False

    update_bullets(mock_game)

    # Inactive bullet should be removed
    assert len(mock_game.bullets) == 0


def test_get_grid_cells_single_cell(mock_game: MockGame) -> None:
    """Test get_grid_cells for object in single cell."""
    rect = pygame.Rect(10, 10, 20, 20)

    cells = get_grid_cells(rect)

    # Small rect should occupy only one cell
    assert len(cells) == 1
    assert (0, 0) in cells


def test_get_grid_cells_multiple_cells(mock_game: MockGame) -> None:
    """Test get_grid_cells for object spanning multiple cells."""
    # Create rect spanning multiple 64-pixel cells
    # Rect from (50,50) to (130,130) covers cells (0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)
    rect = pygame.Rect(50, 50, 80, 80)

    cells = get_grid_cells(rect)

    # Rect covers cells in range: x from 50//64=0 to 130//64=2, y from 50//64=0 to 130//64=2
    # That's 3x3 = 9 cells
    assert len(cells) == 9


def test_get_grid_cells_edge_case(mock_game: MockGame) -> None:
    """Test get_grid_cells at cell boundaries."""
    rect = pygame.Rect(64, 64, 1, 1)

    cells = get_grid_cells(rect)

    # Should be in cell (1, 1)
    assert (1, 1) in cells


def test_update_spatial_grid_empty(mock_game: MockGame) -> None:
    """Test spatial grid update with no objects."""
    mock_game.aliens.empty()
    mock_game.bullets.empty()

    update_spatial_grid(mock_game)

    # Grid should be empty
    assert len(spatial_grid) == 0


def test_update_spatial_grid_with_aliens(mock_game: MockGame) -> None:
    """Test spatial grid update with aliens."""
    create_alien(mock_game, alien_number=0, row_number=0)

    update_spatial_grid(mock_game)

    # Grid should have at least one cell with aliens
    assert len(spatial_grid) > 0
    has_aliens = any(len(cell["aliens"]) > 0 for cell in spatial_grid.values())
    assert has_aliens


def test_update_spatial_grid_with_bullets(mock_game: MockGame) -> None:
    """Test spatial grid update with bullets."""
    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)

    update_spatial_grid(mock_game)

    # Grid should have at least one cell with bullets
    assert len(spatial_grid) > 0
    has_bullets = any(len(cell["bullets"]) > 0 for cell in spatial_grid.values())
    assert has_bullets


def test_update_spatial_grid_with_both(mock_game: MockGame) -> None:
    """Test spatial grid update with both aliens and bullets."""
    create_alien(mock_game, alien_number=0, row_number=0)
    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)

    update_spatial_grid(mock_game)

    # Grid should have cells with both aliens and bullets
    assert len(spatial_grid) > 0


def test_check_bullet_alien_collisions_hit(mock_game: MockGame) -> None:
    """Test that bullet-alien collision is detected."""
    create_alien(mock_game, alien_number=0, row_number=0)
    alien = list(mock_game.aliens.sprites())[0]

    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)

    # Position bullet at alien
    bullet.rect.center = alien.rect.center
    initial_score = mock_game.statistics.score

    check_bullet_alien_collisions(mock_game)

    # Bullet should be inactive
    assert bullet.active is False
    # Alien should be destroyed
    assert alien not in mock_game.aliens
    # Score should increase
    assert mock_game.statistics.score > initial_score


def test_check_bullet_alien_collisions_no_hit(mock_game: MockGame) -> None:
    """Test that no collision is detected when objects are apart."""
    create_alien(mock_game, alien_number=0, row_number=0)
    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)

    initial_score = mock_game.statistics.score

    check_bullet_alien_collisions(mock_game)

    # Bullet should still be active
    assert bullet.active is True
    # Score should not change
    assert mock_game.statistics.score == initial_score


def test_check_bullet_alien_collisions_level_complete(mock_game: MockGame) -> None:
    """Test that level advances when all aliens destroyed."""
    create_alien(mock_game, alien_number=0, row_number=0)
    alien = list(mock_game.aliens.sprites())[0]

    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)
    bullet.rect.center = alien.rect.center

    initial_level = mock_game.statistics.level

    check_bullet_alien_collisions(mock_game)

    # Level should increase
    assert mock_game.statistics.level > initial_level
    # Bullets should be cleared
    assert len(mock_game.bullets) == 0
    # New fleet should be created
    assert len(mock_game.aliens) > 0


def test_check_high_score_new_high(mock_game: MockGame) -> None:
    """Test that high score is updated when exceeded."""
    mock_game.statistics.score = 1000
    mock_game.statistics.high_score = 500

    check_high_score(mock_game)

    assert mock_game.statistics.high_score == 1000


def test_check_high_score_no_change(mock_game: MockGame) -> None:
    """Test that high score is not updated when not exceeded."""
    mock_game.statistics.score = 500
    mock_game.statistics.high_score = 1000

    check_high_score(mock_game)

    assert mock_game.statistics.high_score == 1000


def test_check_fleet_edges_no_edge(mock_game: MockGame) -> None:
    """Test check_fleet_edges when no alien at edge."""
    create_alien(mock_game, alien_number=0, row_number=0)
    alien = list(mock_game.aliens.sprites())[0]
    initial_y = alien.rect.y

    check_fleet_edges(mock_game)

    # Alien should not have moved down
    assert alien.rect.y == initial_y


def test_check_fleet_edges_at_edge(mock_game: MockGame) -> None:
    """Test check_fleet_edges when alien reaches edge."""
    create_alien(mock_game, alien_number=0, row_number=0)
    alien = list(mock_game.aliens.sprites())[0]

    # Move alien to right edge
    screen_rect = mock_game.screen.get_rect()
    alien.rect.right = screen_rect.right

    initial_y = alien.rect.y
    initial_direction = mock_game.ai_configuration.fleet_direction

    check_fleet_edges(mock_game)

    # Fleet should have moved down
    assert alien.rect.y > initial_y
    # Direction should have changed
    assert mock_game.ai_configuration.fleet_direction != initial_direction


def test_change_fleet_direction(mock_game: MockGame) -> None:
    """Test that change_fleet_direction moves fleet down and reverses direction."""
    create_alien(mock_game, alien_number=0, row_number=0)
    create_alien(mock_game, alien_number=1, row_number=0)

    aliens = list(mock_game.aliens.sprites())
    initial_y_positions = [alien.rect.y for alien in aliens]
    initial_direction = mock_game.ai_configuration.fleet_direction

    change_fleet_direction(mock_game)

    # All aliens should have moved down
    for i, alien in enumerate(aliens):
        assert alien.rect.y > initial_y_positions[i]

    # Direction should be reversed
    assert mock_game.ai_configuration.fleet_direction == -initial_direction


def test_change_fleet_direction_multiple_times(mock_game: MockGame) -> None:
    """Test that direction alternates correctly."""
    initial_direction = mock_game.ai_configuration.fleet_direction

    change_fleet_direction(mock_game)
    first_change = mock_game.ai_configuration.fleet_direction

    change_fleet_direction(mock_game)
    second_change = mock_game.ai_configuration.fleet_direction

    # Should alternate
    assert first_change == -initial_direction
    assert second_change == initial_direction
