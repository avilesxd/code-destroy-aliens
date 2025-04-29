from typing import List, Tuple

import pygame.font

from src.config.configuration import Configuration
from src.config.language import Language


class ControlsScreen:
    """A class to display game controls"""

    def __init__(
        self,
        ai_configuration: Configuration,
        screen: pygame.Surface,
        language: Language,
    ) -> None:
        """Initialize the controls screen"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.language = language

        # Set the font and colors
        self.title_font = pygame.font.SysFont(None, 64)
        self.text_font = pygame.font.SysFont(None, 36)
        self.title_color: Tuple[int, int, int] = (0, 255, 0)  # Green
        self.text_color: Tuple[int, int, int] = (255, 255, 255)  # White

        # Create the title
        self.title = self.title_font.render(self.language.get_text("game_controls"), True, self.title_color)
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = 50

        # Create the controls text
        self.controls: List[Tuple[str, str]] = [
            ("Left/Right Arrow", self.language.get_text("move_left_right")),
            ("Space", self.language.get_text("shoot")),
            ("P", self.language.get_text("pause_game")),
            ("Q", self.language.get_text("quit_game")),
        ]

        # Create the continue text
        self.continue_font = pygame.font.SysFont(None, 48)
        self.continue_text = self.continue_font.render(self.language.get_text("press_space"), True, self.text_color)
        self.continue_rect = self.continue_text.get_rect()
        self.continue_rect.centerx = self.screen_rect.centerx
        self.continue_rect.bottom = self.screen_rect.bottom - 50

        # Create a semi-transparent surface for the background
        self.background = pygame.Surface((self.screen_rect.width, self.screen_rect.height), pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 200))  # Black with 78% opacity

    def draw_controls(self) -> None:
        """Draw the controls screen"""
        # Draw the semi-transparent background
        self.screen.blit(self.background, (0, 0))

        # Draw the title
        self.screen.blit(self.title, self.title_rect)

        # Draw each control
        y_position = self.title_rect.bottom + 50
        for key, action in self.controls:
            # Draw the key
            key_text = self.text_font.render(key, True, self.text_color)
            key_rect = key_text.get_rect()
            key_rect.right = self.screen_rect.centerx - 50  # Align right side of key text
            key_rect.top = y_position
            self.screen.blit(key_text, key_rect)

            # Draw the action
            action_text = self.text_font.render(action, True, self.text_color)
            action_rect = action_text.get_rect()
            action_rect.left = self.screen_rect.centerx + 50  # Align left side of action text
            action_rect.top = y_position
            self.screen.blit(action_text, action_rect)

            y_position += 50

        # Draw the continue text
        self.screen.blit(self.continue_text, self.continue_rect)
