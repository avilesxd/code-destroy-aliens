import os

import pygame

# Setting up headless mode for Pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import src.config.rendering.game_rendering as rendering
from src.config.actors.game_actors import create_fleet
from src.config.logic.game_logic import check_bullet_alien_collisions, get_grid_cells, spatial_grid, update_spatial_grid
from src.config.rendering.game_rendering import create_gradient_surface, fire_bullet, stars, update_stars
from src.entities.bullet import Bullet
from tests.conftest import MockGame


def test_create_fleet(mock_game: MockGame) -> None:
    """Test if the alien fleet is created correctly."""
    create_fleet(mock_game)

    assert len(mock_game.aliens) > 0
    # Check if aliens are properly positioned
    for alien in mock_game.aliens:
        assert alien.rect.x >= 0
        assert alien.rect.y >= 0
        assert alien.rect.right <= mock_game.ai_configuration.screen_width
        assert alien.rect.bottom <= mock_game.ai_configuration.screen_height


def test_ship_movement(mock_game: MockGame) -> None:
    """Test if the ship moves correctly."""
    # Test right movement
    initial_x = mock_game.ship.rect.centerx
    mock_game.ship.moving_right = True
    mock_game.ship.moving_left = False
    mock_game.ship.update()
    assert mock_game.ship.rect.centerx > initial_x

    # Test left movement
    mock_game.ship.center = mock_game.ship.screen_rect.centerx  # Reset to center
    mock_game.ship.rect.centerx = mock_game.ship.center  # Update rect position
    initial_x = mock_game.ship.rect.centerx
    mock_game.ship.moving_right = False
    mock_game.ship.moving_left = True
    mock_game.ship.update()
    assert mock_game.ship.rect.centerx < initial_x


def test_bullet_creation(mock_game: MockGame) -> None:
    """Test if bullets are created correctly."""
    initial_bullet_count = len(mock_game.bullets)

    # Create a bullet
    fire_bullet(mock_game)

    assert len(mock_game.bullets) == initial_bullet_count + 1
    for bullet in mock_game.bullets:
        assert bullet.rect.centerx == mock_game.ship.rect.centerx
        assert bullet.rect.top == mock_game.ship.rect.top


def test_collision_bullet_alien(mock_game: MockGame) -> None:
    """Test collision between bullets and aliens."""
    # Create a bullet and an alien
    fire_bullet(mock_game)
    create_fleet(mock_game)

    # Get the first bullet and alien
    bullet = next(iter(mock_game.bullets))
    alien = next(iter(mock_game.aliens))

    # Position bullet and alien to collide
    bullet.rect.center = alien.rect.center

    initial_alien_count = len(mock_game.aliens)

    # Simulate collision
    check_bullet_alien_collisions(mock_game)
    assert len(mock_game.aliens) < initial_alien_count


def test_ship_alien_collision(mock_game: MockGame) -> None:
    """Test collision between ship and aliens."""
    # Create aliens
    create_fleet(mock_game)

    # Get the first alien and position it to collide with ship
    alien = next(iter(mock_game.aliens))
    alien.rect.center = mock_game.ship.rect.center

    # Check collision
    assert pygame.sprite.spritecollideany(mock_game.ship, mock_game.aliens) is not None


def test_score_increment(mock_game: MockGame) -> None:
    """Test score increment when destroying aliens."""
    initial_score = mock_game.statistics.score
    points_per_alien = mock_game.ai_configuration.alien_points

    # Create and destroy an alien
    create_fleet(mock_game)
    if len(mock_game.aliens) > 0:
        alien = mock_game.aliens.sprites()[0]
        alien.kill()
        mock_game.statistics.score += points_per_alien

    assert mock_game.statistics.score == initial_score + points_per_alien


def test_game_pause(mock_game: MockGame) -> None:
    """Test game pause functionality."""
    # Simulate pause
    mock_game.statistics.game_paused = True
    initial_ship_x = mock_game.ship.rect.centerx

    # Try to move ship while paused
    mock_game.ship.moving_right = True
    mock_game.ship.update()

    assert mock_game.ship.rect.centerx == initial_ship_x
    assert mock_game.statistics.game_paused is True


def test_game_over(mock_game: MockGame) -> None:
    """Test game over conditions."""
    # Simulate game over
    mock_game.statistics.game_active = False
    mock_game.statistics.ships_remaining = 0

    assert mock_game.statistics.game_active is False
    assert mock_game.statistics.ships_remaining == 0
    assert mock_game.play_button.rect.centerx == mock_game.screen.get_rect().centerx
    assert mock_game.play_button.rect.centery == mock_game.screen.get_rect().centery


def test_bullet_pooling(mock_game: MockGame) -> None:
    """Test the bullet pooling system."""
    # Create initial bullets
    for _ in range(5):
        fire_bullet(mock_game)

    initial_bullet_count = len(mock_game.bullets)

    # Remove bullets (they should go to the pool)
    for bullet in mock_game.bullets.sprites():
        bullet.active = False
        Bullet.return_to_pool(bullet)

    # Create new bullets (should reuse from pool)
    for _ in range(5):
        fire_bullet(mock_game)

    # Verify that bullets are being reused
    assert len(Bullet._bullet_pool) <= Bullet._max_pool_size
    assert len(mock_game.bullets) == initial_bullet_count


def test_spatial_grid(mock_game: MockGame) -> None:
    """Test the spatial grid system for collision detection."""
    # Create a bullet and an alien
    fire_bullet(mock_game)
    create_fleet(mock_game)

    # Get the first bullet and alien
    bullet = next(iter(mock_game.bullets))
    alien = next(iter(mock_game.aliens))

    # Position bullet and alien in the same grid cell
    bullet.rect.center = alien.rect.center

    # Update spatial grid
    update_spatial_grid(mock_game)

    # Get the grid cells for the bullet and alien
    bullet_cells = get_grid_cells(bullet.rect)
    alien_cells = get_grid_cells(alien.rect)

    # Verify that they share at least one grid cell
    shared_cells = set(bullet_cells) & set(alien_cells)
    assert len(shared_cells) > 0

    # Verify that the collision is detected in the shared cell
    for cell in shared_cells:
        if cell in spatial_grid:
            cell_data = spatial_grid[cell]
            assert bullet in cell_data["bullets"]
            assert alien in cell_data["aliens"]


def test_gradient_caching(mock_game: MockGame) -> None:
    """Test the gradient caching system."""
    # Create gradient twice with same screen size
    gradient1 = create_gradient_surface(
        mock_game.screen,
        mock_game.ai_configuration.gradient_top_color,
        mock_game.ai_configuration.gradient_bottom_color,
    )
    gradient2 = create_gradient_surface(
        mock_game.screen,
        mock_game.ai_configuration.gradient_top_color,
        mock_game.ai_configuration.gradient_bottom_color,
    )

    # Verify that the same cached gradient is returned
    assert gradient1 is gradient2
    assert rendering.cached_gradient is not None

    # Change screen size and create new gradient
    new_screen = pygame.display.set_mode(
        (mock_game.ai_configuration.screen_width + 100, mock_game.ai_configuration.screen_height + 100)
    )
    gradient3 = create_gradient_surface(
        new_screen,
        mock_game.ai_configuration.gradient_top_color,
        mock_game.ai_configuration.gradient_bottom_color,
    )

    # Verify that a new gradient is created
    assert gradient3 is not gradient1
    assert gradient3 is not gradient2


def test_star_system(mock_game: MockGame) -> None:
    """Test the optimized star system."""
    # Initialize stars
    update_stars(mock_game)

    # Verify that stars are created
    assert len(stars) == mock_game.ai_configuration.star_count

    # Verify star properties
    for star in stars:
        x, y, size, speed = star
        assert 0 <= x <= mock_game.ai_configuration.screen_width
        assert 0 <= y <= mock_game.ai_configuration.screen_height
        assert 1 <= size <= 3
        assert 0.1 <= speed <= 0.5

    # Test star movement
    initial_positions = [(star[0], star[1]) for star in stars]
    rendering.last_star_time = pygame.time.get_ticks() - 17  # Force update
    update_stars(mock_game)

    # Verify that stars have moved
    for i, star in enumerate(stars):
        assert (star[0], star[1]) != initial_positions[i]
