import pytest
import pygame
from pygame.sprite import Group
from src.config.configuration import Configuration
from src.config.statistics import Statistics
from src.config.language import Language
from src.entities.ship import Ship
from src.entities.button import Button
import src.config.game_functions as fj

@pytest.fixture
def game_components():
    """Set up game components for testing."""
    pygame.init()
    config = Configuration()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    stats = Statistics(config)
    language = Language()
    ship = Ship(config, screen, stats)
    bullets = Group()
    aliens = Group()
    play_button = Button(config, screen, language.get_text("play"))
    return config, screen, stats, ship, bullets, aliens, play_button

def test_create_fleet(game_components):
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

def test_ship_movement(game_components):
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

def test_bullet_creation(game_components):
    """Test if bullets are created correctly."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components
    initial_bullet_count = len(bullets)
    
    # Create a bullet
    fj.fire_bullet(config, screen, ship, bullets)
    
    assert len(bullets) == initial_bullet_count + 1
    for bullet in bullets:
        assert bullet.rect.centerx == ship.rect.centerx
        assert bullet.rect.top == ship.rect.top 

def test_collision_bullet_alien(game_components):
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

def test_ship_alien_collision(game_components):
    """Test collision between ship and aliens."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components

    # Create aliens
    fj.create_fleet(config, screen, ship, aliens)

    # Get the first alien and position it to collide with ship
    alien = next(iter(aliens))
    alien.rect.center = ship.rect.center

    # Check collision
    assert pygame.sprite.spritecollideany(ship, aliens) is not None

def test_score_increment(game_components):
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

def test_game_pause(game_components):
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

def test_game_over(game_components):
    """Test game over conditions."""
    config, screen, stats, ship, bullets, aliens, play_button = game_components
    
    # Simulate game over
    stats.game_active = False
    stats.ships_left = 0
    
    assert stats.game_active == False
    assert stats.ships_left == 0
    assert play_button.rect.centerx == screen.get_rect().centerx
    assert play_button.rect.centery == screen.get_rect().centery 