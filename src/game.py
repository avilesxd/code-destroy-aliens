import pygame
from pygame.sprite import Group

from src.config.actors.game_actors import create_fleet
from src.config.configuration import Configuration
from src.config.controls.game_controls import verify_events
from src.config.language.language import Language
from src.config.logic.game_logic import update_aliens, update_bullets
from src.config.music.music import Music
from src.config.rendering.game_rendering import update_screen
from src.config.statistics.statistics import Statistics
from src.core.path_utils import resource_path
from src.entities.button import Button
from src.entities.controls_screen import ControlsScreen
from src.entities.scoreboard import Scoreboard
from src.entities.ship import Ship


class Game:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        """Initialize the game, and create game resources."""
        pygame.init()
        self.music = Music()
        self.ai_configuration = Configuration()
        self.screen = pygame.display.set_mode(
            (self.ai_configuration.screen_width, self.ai_configuration.screen_height), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.fps_counter = None
        pygame.display.set_caption("Alien Invasion")

        # Set window icon
        icon_path = resource_path("src/assets/icons/icon.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        self.language = Language()
        self.play_button = Button(self.ai_configuration, self.screen, self.language.get_text("play"))
        self.statistics = Statistics(self.ai_configuration)
        self.scoreboard = Scoreboard(self.ai_configuration, self.screen, self.statistics, self.language)
        self.controls_screen = ControlsScreen(self.ai_configuration, self.screen, self.language)
        self.ship = Ship(self.ai_configuration, self.screen, self.statistics, self.music)
        self.bullets: Group = Group()
        self.aliens: Group = Group()

        create_fleet(self)

    def run(self) -> None:
        """Start the main loop for the game."""
        while True:
            self.clock.tick(60)
            fps = int(self.clock.get_fps())
            self.fps_counter = self.font.render(f"FPS: {fps}", True, (255, 255, 255))

            verify_events(self)

            if self.statistics.game_active and not self.statistics.game_paused:
                self.ship.update()
                update_bullets(self)
                update_aliens(self)

            update_screen(self)
