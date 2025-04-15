import sys
from time import sleep
import pygame
from src.entities.bullet import Bullet
from src.entities.alien import Alien
from src.entities.ship import Ship
from src.config.statistics import Statistics as statistics


def verify_events_keydown(event, ai_configuration, screen, ship, bullets, statistics, music):
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
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


def verify_events_keyup(event, ship):
    """Responds to keystrokes"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def verify_events(
    ai_configuration, screen, statistics, scoreboard, play_button, ship, aliens, bullets, music
):
    """Responds to keystrokes and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            verify_events_keydown(event, ai_configuration, screen, ship, bullets, statistics, music)

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
):
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
    ai_configuration, screen, statistics, scoreboard, ship, aliens, bullets, play_button
):
    """Updates the images on the screen and switches to the new screen"""

    # Redraws the screen during each loop
    screen.fill(ai_configuration.bg_color)
    # Redraws all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    scoreboard.show_score()

    # Draw the Play button if the game is inactive
    if not statistics.game_active:
        play_button.draw_button()

    # Make the most recent screen visible
    pygame.display.flip()


def update_bullets(
    ai_configuration, screen, statistics, scoreboard, ship, aliens, bullets
):
    """Updates the bullet positions and removes old ones"""
    # Updates the bullet positions
    bullets.update()

    # Undoes bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_configuration, screen, statistics, scoreboard, ship, aliens, bullets
    )


def check_bullet_alien_collisions(
    ai_configuration, screen, statistics, scoreboard, ship, aliens, bullets
):
    """Responds to collisions between bullets and aliens"""
    # Remove colliding bullets and aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            statistics.score += ai_configuration.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(statistics, scoreboard)

    if len(aliens) == 0:
        # Destroy existing bullets and create a new fleet
        bullets.empty()

        # We only increase speed when a level is completed
        # Not every time an alien is eliminated
        ai_configuration.boost_speed()

        # Increases level
        statistics.level += 1
        scoreboard.prep_level()

        create_fleet(ai_configuration, screen, ship, aliens)


def check_high_score(statistics, scoreboard):
    """Checks if a higher score exists"""
    if statistics.score > statistics.high_score:
        statistics.high_score = statistics.score
        scoreboard.prep_high_score()


def fire_bullet(ai_configuration, display, ship, bullets):
    """Fire a bullet if it hasn't reached the limit yet"""
    # Create a new bullet and add it to the bullet pool
    if len(bullets) < ai_configuration.bullets_allowed:
        new_bullet = Bullet(ai_configuration, display, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_configuration, alien_width):
    """Determines the number of aliens that fit in a row"""
    available_space_x = ai_configuration.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_configuration, ship_height, alien_height):
    """Determines the number of rows of aliens that fit on the screen"""
    available_space_y = (
        ai_configuration.screen_height - (3 * alien_height) - ship_height
    )
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_configuration, screen, aliens, alien_number, row_number):
    """Create an alien and queue it up"""
    alien = Alien(ai_configuration, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_configuration, screen, ship, aliens):
    """Create an entire fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    # The space between each alien is equal to one width of the alien
    alien = Alien(ai_configuration, screen)
    number_aliens_x = get_number_aliens_x(ai_configuration, alien.rect.width)
    number_rows = get_number_rows(ai_configuration, ship.rect.height, alien.rect.height)

    # Create the alien fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_configuration, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_configuration, aliens):
    """Respond appropriately if any alien has reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_configuration, aliens)
            break


def change_fleet_direction(ai_configuration, aliens):
    """Drops the entire fleet and changes the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_configuration.fleet_drop_speed
    ai_configuration.fleet_direction *= -1


def ship_hit(ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets):
    """Responds to a ship being hit by an alien"""

    if statistics.ships_remaining > 0:
        # Decrease ships_remaining
        statistics.ships_remaining -= 1

        # Update the scoreboard
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
        statistics.game_paused = False  # Reset pause state when game ends
        pygame.mouse.set_visible(True)


def check_aliens_bottom(
    ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets
):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship were hit
            ship_hit(
                ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets
            )
            break


def update_aliens(
    ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets
):
    """Checks if the fleet is at the edge and then updates the positions of all aliens in the fleet"""
    check_fleet_edges(ai_configuration, aliens)
    aliens.update()

    # Check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(
            ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets
        )

    # Check for aliens hitting the bottom of the screen
    check_aliens_bottom(
        ai_configuration, statistics, screen, scoreboard, ship, aliens, bullets
    )
