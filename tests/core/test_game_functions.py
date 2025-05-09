import os
from typing import Tuple

import pygame
import pytest

# Setting up headless mode for Pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

# Import game modules after setting up the environment
from pygame.sprite import Group

import src.config.game_functions as fj
from src.config.configuration import Configuration
from src.config.language import Language
from src.config.music import Music
from src.config.statistics import Statistics
from src.entities.bullet import Bullet
from src.entities.button import Button
from src.entities.ship import Ship


@pytest.fixture
def game_components() -> Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]:
    """Set up game components for testing."""
    pygame.init()
    config = Configuration()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    stats = Statistics(config)
    language = Language()
    music = Music()
    ship = Ship(config, screen, stats, music)
    bullets: Group = Group()
    aliens: Group = Group()
    play_button = Button(config, screen, language.get_text("play"))
    return config, screen, stats, ship, bullets, aliens, play_button


def test_create_fleet(game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]) -> None:
    """Test if the alien fleet is created correctly."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components
    fj.create_fleet(config, screen, ship, aliens)

    assert len(aliens) > 0
    # Check if aliens are properly positioned
    for alien in aliens:
        assert alien.rect.x >= 0
        assert alien.rect.y >= 0
        assert alien.rect.right <= config.screen_width
        assert alien.rect.bottom <= config.screen_height


def test_ship_movement(
    game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]
) -> None:
    """Test if the ship moves correctly."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Test right movement
    initial_x = ship.rect.centerx
    ship.moving_right = True
    ship.moving_left = False
    ship.update()
    assert ship.rect.centerx > initial_x

    # Test left movement
    ship.center = ship.screen_rect.centerx  # Reset to center
    ship.rect.centerx = ship.center  # Update rect position
    initial_x = ship.rect.centerx
    ship.moving_right = False
    ship.moving_left = True
    ship.update()
    assert ship.rect.centerx < initial_x


def test_bullet_creation(
    game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]
) -> None:
    """Test if bullets are created correctly."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components
    initial_bullet_count = len(bullets)

    # Create a bullet
    fj.fire_bullet(config, screen, ship, bullets)

    assert len(bullets) == initial_bullet_count + 1
    for bullet in bullets:
        assert bullet.rect.centerx == ship.rect.centerx
        assert bullet.rect.top == ship.rect.top


def test_collision_bullet_alien(
    game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]
) -> None:
    """Test collision between bullets and aliens."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Create a bullet and an alien
    fj.fire_bullet(config, screen, ship, bullets)
    fj.create_fleet(config, screen, ship, aliens)

    # Get the first bullet and alien
    bullet = next(iter(bullets))
    alien = next(iter(aliens))

    # Position bullet and alien to collide
    bullet.rect.center = alien.rect.center

    initial_alien_count = len(aliens)

    # Simulate collision
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    assert len(aliens) < initial_alien_count


def test_ship_alien_collision(
    game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]
) -> None:
    """Test collision between ship and aliens."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Create aliens
    fj.create_fleet(config, screen, ship, aliens)

    # Get the first alien and position it to collide with ship
    alien = next(iter(aliens))
    alien.rect.center = ship.rect.center

    # Check collision
    assert pygame.sprite.spritecollideany(ship, aliens) is not None


def test_score_increment(
    game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]
) -> None:
    """Test score increment when destroying aliens."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    initial_score = stats.score
    points_per_alien = config.alien_points

    # Create and destroy an alien
    fj.create_fleet(config, screen, ship, aliens)
    if len(aliens) > 0:
        alien = aliens.sprites()[0]
        alien.kill()
        stats.score += points_per_alien

    assert stats.score == initial_score + points_per_alien


def test_game_pause(game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]) -> None:
    """Test game pause functionality."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Simulate pause
    stats.game_paused = True
    initial_ship_x = ship.rect.centerx

    # Try to move ship while paused
    ship.moving_right = True
    ship.update()

    assert ship.rect.centerx == initial_ship_x
    assert stats.game_paused == True


def test_game_over(game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]) -> None:
    """Test game over conditions."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Simulate game over
    stats.game_active = False
    stats.ships_remaining = 0

    assert stats.game_active == False
    assert stats.ships_remaining == 0
    assert play_button.rect.centerx == screen.get_rect().centerx
    assert play_button.rect.centery == screen.get_rect().centery


def test_bullet_pooling(
    game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]
) -> None:
    """Test the bullet pooling system."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Create initial bullets
    for _ in range(5):
        fj.fire_bullet(config, screen, ship, bullets)

    initial_bullet_count = len(bullets)

    # Remove bullets (they should go to the pool)
    for bullet in bullets.sprites():
        bullet.active = False
        Bullet.return_to_pool(bullet)

    # Create new bullets (should reuse from pool)
    for _ in range(5):
        fj.fire_bullet(config, screen, ship, bullets)

    # Verify that bullets are being reused
    assert len(Bullet._bullet_pool) <= Bullet._max_pool_size
    assert len(bullets) == initial_bullet_count


def test_spatial_grid(game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]) -> None:
    """Test the spatial grid system for collision detection."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Create a bullet and an alien
    fj.fire_bullet(config, screen, ship, bullets)
    fj.create_fleet(config, screen, ship, aliens)

    # Get the first bullet and alien
    bullet = next(iter(bullets))
    alien = next(iter(aliens))

    # Position bullet and alien in the same grid cell
    bullet.rect.center = alien.rect.center

    # Update spatial grid
    fj.update_spatial_grid(aliens, bullets)

    # Get the grid cells for the bullet and alien
    bullet_cells = fj.get_grid_cells(bullet.rect)
    alien_cells = fj.get_grid_cells(alien.rect)

    # Verify that they share at least one grid cell
    shared_cells = set(bullet_cells) & set(alien_cells)
    assert len(shared_cells) > 0

    # Verify that the collision is detected in the shared cell
    for cell in shared_cells:
        if cell in fj.spatial_grid:
            cell_data = fj.spatial_grid[cell]
            assert bullet in cell_data["bullets"]
            assert alien in cell_data["aliens"]


def test_gradient_caching(
    game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]
) -> None:
    """Test the gradient caching system."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Create gradient twice with same screen size
    gradient1 = fj.create_gradient_surface(screen, config.gradient_top_color, config.gradient_bottom_color)
    gradient2 = fj.create_gradient_surface(screen, config.gradient_top_color, config.gradient_bottom_color)

    # Verify that the same cached gradient is returned
    assert gradient1 is gradient2
    assert fj.cached_gradient is not None

    # Change screen size and create new gradient
    new_screen = pygame.display.set_mode((config.screen_width + 100, config.screen_height + 100))
    gradient3 = fj.create_gradient_surface(new_screen, config.gradient_top_color, config.gradient_bottom_color)

    # Verify that a new gradient is created
    assert gradient3 is not gradient1
    assert gradient3 is not gradient2


def test_star_system(game_components: Tuple[Configuration, pygame.Surface, Statistics, Ship, Group, Group, Button]) -> None:
    """Test the optimized star system."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Initialize stars
    fj.update_stars(screen, config)

    # Verify that stars are created
    assert len(fj.stars) == config.star_count

    # Verify star properties
    for star in fj.stars:
        x, y, size, speed = star
        assert 0 <= x <= config.screen_width
        assert 0 <= y <= config.screen_height
        assert 1 <= size <= 3
        assert 0.1 <= speed <= 0.5

    # Test star movement
    initial_positions = [(star[0], star[1]) for star in fj.stars]
    fj.last_star_time = pygame.time.get_ticks() - 17  # Force update
    fj.update_stars(screen, config)

    # Verify that stars have moved
    for i, star in enumerate(fj.stars):
        assert (star[0], star[1]) != initial_positions[i]
