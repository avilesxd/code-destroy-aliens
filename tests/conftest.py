import os

import pygame
import pytest

# Setting up headless mode for Pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from pygame.sprite import Group

from src.config.configuration import Configuration
from src.config.language.language import Language
from src.config.music.music import Music
from src.config.statistics.statistics import Statistics
from src.entities.button import Button
from src.entities.controls_screen import ControlsScreen
from src.entities.scoreboard import Scoreboard
from src.entities.ship import Ship
from src.game import Game


# Helper class to mock the Game object
class MockGame(Game):
    def __init__(self) -> None:
        pygame.init()
        self.ai_configuration = Configuration()
        self.screen = pygame.display.set_mode((self.ai_configuration.screen_width, self.ai_configuration.screen_height))
        self.statistics = Statistics(self.ai_configuration)
        self.language = Language()
        self.music = Music()
        self.ship = Ship(self.ai_configuration, self.screen, self.statistics, self.music)
        self.bullets: Group = Group()
        self.aliens: Group = Group()
        self.play_button = Button(self.ai_configuration, self.screen, self.language.get_text("play"))
        self.scoreboard = Scoreboard(self.ai_configuration, self.screen, self.statistics, self.language)
        self.controls_screen = ControlsScreen(self.ai_configuration, self.screen, self.language)


@pytest.fixture
def mock_game() -> MockGame:
    """Set up a mock game object for testing."""
    return MockGame()
