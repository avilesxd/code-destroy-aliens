import random
import sys
from time import sleep
from typing import Dict, List, Optional, Tuple, Union

import pygame
from pygame.sprite import Group

from src.config.configuration import Configuration
from src.config.music import Music
from src.config.statistics import Statistics
from src.entities.alien import Alien
from src.entities.bullet import Bullet
from src.entities.button import Button
from src.entities.controls_screen import ControlsScreen
from src.entities.scoreboard import Scoreboard
from src.entities.ship import Ship

# Global variables for stars and gradient
stars: List[List[Union[int, float]]] = []  # List to store star positions and properties
last_star_time: int = 0  # Timestamp of the last star creation
cached_gradient: Optional[pygame.Surface] = None  # Cached gradient surface to avoid recreation
last_screen_size: Optional[Tuple[int, int]] = None  # Last screen dimensions used for gradient

# Global variables for spatial grid
spatial_grid: Dict[tuple, Dict[str, List]] = {}  # Dictionary to store objects in a spatial grid for collision detection
grid_cell_size = 64  # Size of each grid cell in pixels for spatial partitioning


def create_gradient_surface(screen: pygame.Surface, top_color: tuple, bottom_color: tuple) -> pygame.Surface:
    """Creates a surface with a vertical gradient from top_color to bottom_color.

    Args:
        screen (pygame.Surface): The screen surface to get dimensions from
        top_color (tuple): RGB color tuple for the top of the gradient
        bottom_color (tuple): RGB color tuple for the bottom of the gradient

    Returns:
        pygame.Surface: A surface with the gradient applied

    Note:
        This function caches the gradient surface to improve performance
        when the screen size hasn't changed.
    """
    global cached_gradient, last_screen_size

    # Check if we can reuse the cached gradient
    current_size = (screen.get_width(), screen.get_height())
    if cached_gradient and last_screen_size == current_size:
        return cached_gradient

    # Create new gradient if needed
    gradient = pygame.Surface(current_size)
    for y in range(current_size[1]):
        ratio = y / current_size[1]
        color = [int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio) for i in range(3)]
        pygame.draw.line(gradient, color, (0, y), (current_size[0], y))

    # Cache the gradient
    cached_gradient = gradient
    last_screen_size = current_size

    return gradient


def update_stars(
    screen: pygame.Surface,
    ai_configuration: Configuration,
    is_paused: bool = False,
    is_game_over: bool = False,
) -> None:
    """Updates and draws the stars"""
    global stars, last_star_time

    # Create initial stars if they don't exist
    if not stars:
        for _ in range(ai_configuration.star_count):
            x = random.randint(0, ai_configuration.screen_width)
            y = random.randint(0, ai_configuration.screen_height)
            size = random.randint(1, 3)
            speed = random.uniform(0.1, 0.5)
            stars.append([x, y, size, speed])

    # Update star positions only if enough time has passed and game is not paused
    if not is_paused and not is_game_over:
        for star in stars:
            star[1] += star[3]  # Move the star downward
            if star[1] > ai_configuration.screen_height:
                star[1] = 0
                star[0] = random.randint(0, ai_configuration.screen_width)

    # Draw the stars
    for star_x, star_y, star_size, _ in stars:
        x_int: int = int(star_x)
        y_int: int = int(star_y)
        size_int: int = int(star_size)
        pygame.draw.circle(screen, ai_configuration.star_color, (x_int, y_int), size_int)


def verify_events_keydown(
    event: pygame.event.Event,
    ai_configuration: Configuration,
    screen: pygame.Surface,
    ship: Ship,
    bullets: Group,
    statistics: Statistics,
    music: Music,
) -> None:
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if statistics.show_controls:
            statistics.show_controls = False
            statistics.controls_seen = True  # Mark controls as seen
        else:
            fire_bullet(ai_configuration, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        # Toggle pause state
        statistics.game_paused = not statistics.game_paused
        # Pause/resume music
        if statistics.game_paused:
            music.pause()
        else:
            music.resume()


def verify_events_keyup(event: pygame.event.Event, ship: Ship) -> None:
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def verify_events(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    play_button: Button,
    ship: Ship,
    aliens: Group,
    bullets: Group,
    music: Music,
) -> None:
    """Responds to keystrokes and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            verify_events_keydown(
                event,
                ai_configuration,
                screen,
                ship,
                bullets,
                statistics,
                music,
            )

        elif event.type == pygame.KEYUP:
            verify_events_keyup(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_configuration,
                screen,
                statistics,
                scoreboard,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_play_button(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    play_button: Button,
    ship: Ship,
    aliens: Group,
    bullets: Group,
    mouse_x: int,
    mouse_y: int,
) -> None:
    """Starts a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not statistics.game_active:
        # Resets the game configuration
        ai_configuration.initialize_dynamic_configurations()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Resets the game statistics
        statistics.reset_stats()
        statistics.game_active = True
        statistics.game_paused = False  # Reset pause state

        # Resets the scoreboard images
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_configuration, screen, ship, aliens)
        ship.center_ship()


def update_screen(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    statistics: Statistics,
    scoreboard: Scoreboard,
    ship: Ship,
    aliens: Group,
    bullets: Group,
    play_button: Button,
    controls_screen: ControlsScreen,
) -> None:
    """Updates the images on the screen and switches to the new screen"""

    if ai_configuration.use_gradient_background:
        # Create and draw the gradient
        gradient = create_gradient_surface(
            screen,
            ai_configuration.gradient_top_color,
            ai_configuration.gradient_bottom_color,
        )
        screen.blit(gradient, (0, 0))

        # Update and draw stars if they are enabled
        if ai_configuration.use_stars:
            update_stars(screen, ai_configuration, statistics.game_paused, statistics.game_over)
    else:
        # Use solid background color if gradient is disabled
        screen.fill(ai_configuration.bg_color)

    # Redraws all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    scoreboard.show_score()

    # Draw the controls screen if it's active
    if statistics.show_controls:
        controls_screen.draw_controls()
    # Draw the Play button if the game is inactive and controls are not showing
    elif not statistics.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


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


def fire_bullet(
    ai_configuration: Configuration,
    screen: pygame.Surface,
    ship: Ship,
    bullets: Group,
) -> None:
    """Creates and fires a new bullet if the bullet limit hasn't been reached.

    Args:
        ai_configuration (Settings): Game configuration settings
        screen (pygame.Surface): The game screen
        ship (Ship): Player's ship
        bullets (pygame.sprite.Group): Group of bullet sprites
    """
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_configuration.bullets_allowed:
        new_bullet = Bullet.get_bullet(ai_configuration, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_configuration: Configuration, alien_width: int) -> int:
    """Calculates how many aliens can fit in a single row.

    Args:
        ai_configuration (Settings): Game configuration settings
        alien_width (int): Width of an alien sprite

    Returns:
        int: Number of aliens that can fit in a row

    The calculation takes into account the screen width and leaves space
    for margins on both sides.
    """
    available_space_x = ai_configuration.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_configuration: Configuration, ship_height: int, alien_height: int) -> int:
    """Calculates how many rows of aliens can fit on the screen.

    Args:
        ai_configuration (Settings): Game configuration settings
        ship_height (int): Height of the ship sprite
        alien_height (int): Height of an alien sprite

    Returns:
        int: Number of rows of aliens that can fit on the screen

    The calculation takes into account the screen height, ship height,
    and leaves space for margins.
    """
    available_space_y = ai_configuration.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


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
