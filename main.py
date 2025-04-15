import pygame
from pygame.sprite import Group
from src.config.configuration import Configuration
from src.config.statistics import Statistics
from src.entities.scoreboard import Scoreboard
from src.entities.button import Button
from src.entities.ship import Ship
from src.config.music import Music
import src.config.game_functions as fj
from src.core.utils import resource_path


# Game window icon
icon_path = resource_path("src/assets/icons/icon.png")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)


def runGame():
    # Initialize the game, settings and create a screen object
    pygame.init()
    # Function to play music
    music = Music()
    ai_configuration = Configuration()
    screen = pygame.display.set_mode(
        (ai_configuration.screen_width, ai_configuration.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Create the Play button
    play_button = Button(ai_configuration, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard
    statistics = Statistics(ai_configuration)
    scoreboard = Scoreboard(ai_configuration, screen, statistics)

    # Create a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_configuration, screen)
    bullet = Group()
    aliens = Group()

    # Create the alien fleet
    fj.create_fleet(ai_configuration, screen, ship, aliens)

    # Start the main game loop
    while True:
        # Listen for keyboard or mouse events
        fj.verify_events(
            ai_configuration,
            screen,
            statistics,
            scoreboard,
            play_button,
            ship,
            aliens,
            bullet,
            music,
        )

        if statistics.game_active and not statistics.game_paused:
            ship.update()
            fj.update_bullets(
                ai_configuration, screen, statistics, scoreboard, ship, aliens, bullet
            )
            fj.update_aliens(
                ai_configuration, statistics, screen, scoreboard, ship, aliens, bullet
            )

        fj.update_screen(
            ai_configuration,
            screen,
            statistics,
            scoreboard,
            ship,
            aliens,
            bullet,
            play_button,
        )


runGame()
