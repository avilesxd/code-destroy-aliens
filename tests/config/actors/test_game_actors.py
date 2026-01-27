"""Tests for game actors module."""

import pygame
from pygame.sprite import Group

from src.config.actors.game_actors import check_aliens_bottom, create_alien, create_fleet, ship_hit
from tests.conftest import MockGame


def test_create_alien(mock_game: MockGame) -> None:
    """Test that create_alien creates an alien at the correct position."""
    initial_alien_count = len(mock_game.aliens)

    create_alien(mock_game, alien_number=0, row_number=0)

    assert len(mock_game.aliens) == initial_alien_count + 1
    alien = list(mock_game.aliens.sprites())[0]
    assert alien.rect.x >= 0
    assert alien.rect.y >= 0


def test_create_alien_positioning(mock_game: MockGame) -> None:
    """Test that aliens are positioned correctly in columns."""
    create_alien(mock_game, alien_number=0, row_number=0)
    create_alien(mock_game, alien_number=1, row_number=0)

    aliens = list(mock_game.aliens.sprites())
    # Second alien should be to the right of first
    assert aliens[1].rect.x > aliens[0].rect.x


def test_create_alien_row_positioning(mock_game: MockGame) -> None:
    """Test that aliens are positioned correctly in rows."""
    create_alien(mock_game, alien_number=0, row_number=0)
    create_alien(mock_game, alien_number=0, row_number=1)

    aliens = list(mock_game.aliens.sprites())
    # Second alien should be below first
    assert aliens[1].rect.y > aliens[0].rect.y


def test_create_fleet(mock_game: MockGame) -> None:
    """Test that create_fleet creates multiple aliens."""
    mock_game.aliens.empty()

    create_fleet(mock_game)

    # Fleet should have at least one alien
    assert len(mock_game.aliens) > 0


def test_create_fleet_multiple_rows(mock_game: MockGame) -> None:
    """Test that fleet has multiple rows of aliens."""
    mock_game.aliens.empty()

    create_fleet(mock_game)

    # Check that aliens have different y positions (multiple rows)
    y_positions = set(alien.rect.y for alien in mock_game.aliens.sprites())
    assert len(y_positions) > 1


def test_create_fleet_multiple_columns(mock_game: MockGame) -> None:
    """Test that fleet has multiple columns of aliens."""
    mock_game.aliens.empty()

    create_fleet(mock_game)

    # Check that aliens have different x positions (multiple columns)
    x_positions = set(alien.rect.x for alien in mock_game.aliens.sprites())
    assert len(x_positions) > 1


def test_ship_hit_decrements_ships_remaining(mock_game: MockGame) -> None:
    """Test that ship_hit decrements ships remaining."""
    initial_ships = mock_game.statistics.ships_remaining
    create_fleet(mock_game)

    ship_hit(mock_game)

    assert mock_game.statistics.ships_remaining == initial_ships - 1


def test_ship_hit_clears_aliens_and_bullets(mock_game: MockGame) -> None:
    """Test that ship_hit clears all aliens and bullets."""
    create_fleet(mock_game)
    # Add some bullets
    from src.entities.bullet import Bullet

    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    mock_game.bullets.add(bullet)

    ship_hit(mock_game)

    # Should create new fleet, so aliens won't be empty
    # but bullets should be cleared and recreated
    assert len(mock_game.bullets) == 0


def test_ship_hit_creates_new_fleet(mock_game: MockGame) -> None:
    """Test that ship_hit creates a new fleet."""
    mock_game.aliens.empty()

    ship_hit(mock_game)

    # New fleet should be created
    assert len(mock_game.aliens) > 0


def test_ship_hit_centers_ship(mock_game: MockGame) -> None:
    """Test that ship_hit centers the ship."""
    # Move ship to the right
    mock_game.ship.center = 500.0
    mock_game.ship.rect.centerx = 500

    ship_hit(mock_game)

    # Ship should be centered
    screen_rect = mock_game.screen.get_rect()
    assert abs(mock_game.ship.rect.centerx - screen_rect.centerx) < 5


def test_ship_hit_game_over(mock_game: MockGame) -> None:
    """Test that ship_hit triggers game over when no ships remain."""
    mock_game.statistics.ships_remaining = 0
    mock_game.statistics.game_active = True

    ship_hit(mock_game)

    assert mock_game.statistics.ships_remaining == 0
    assert mock_game.statistics.game_active is False


def test_ship_hit_with_zero_ships(mock_game: MockGame) -> None:
    """Test ship_hit when already at zero ships."""
    mock_game.statistics.ships_remaining = 0
    mock_game.statistics.game_active = True

    ship_hit(mock_game)

    assert mock_game.statistics.game_active is False


def test_check_aliens_bottom_no_collision(mock_game: MockGame) -> None:
    """Test check_aliens_bottom when no aliens reached bottom."""
    create_fleet(mock_game)
    initial_ships = mock_game.statistics.ships_remaining

    # Aliens should be at top, not bottom
    check_aliens_bottom(mock_game)

    # Ships remaining should not change
    assert mock_game.statistics.ships_remaining == initial_ships


def test_check_aliens_bottom_with_collision(mock_game: MockGame) -> None:
    """Test check_aliens_bottom when alien reaches bottom."""
    create_alien(mock_game, alien_number=0, row_number=0)
    initial_ships = mock_game.statistics.ships_remaining

    # Move alien to bottom of screen
    screen_rect = mock_game.screen.get_rect()
    alien = list(mock_game.aliens.sprites())[0]
    alien.rect.bottom = screen_rect.bottom

    check_aliens_bottom(mock_game)

    # Should trigger ship_hit
    assert mock_game.statistics.ships_remaining == initial_ships - 1


def test_check_aliens_bottom_stops_after_first_hit(mock_game: MockGame) -> None:
    """Test that check_aliens_bottom stops after first collision."""
    # Create multiple aliens at bottom
    screen_rect = mock_game.screen.get_rect()

    for i in range(3):
        create_alien(mock_game, alien_number=i, row_number=0)

    # Move all aliens to bottom
    for alien in mock_game.aliens.sprites():
        alien.rect.bottom = screen_rect.bottom

    initial_ships = mock_game.statistics.ships_remaining

    check_aliens_bottom(mock_game)

    # Should only decrement ships once (breaks after first hit)
    assert mock_game.statistics.ships_remaining == initial_ships - 1
