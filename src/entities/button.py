from typing import Tuple

import pygame.font

from src.config.configuration import Configuration


class Button:
    """A class to create and manage clickable buttons in the game.

    This class handles the creation, rendering, and positioning of buttons
    with customizable text and colors.

    Attributes:
        screen (pygame.Surface): The game screen surface
        screen_rect (pygame.Rect): The screen's rectangle
        width (int): Button width in pixels
        height (int): Button height in pixels
        button_color (tuple): RGB color of the button
        text_color (tuple): RGB color of the button text
        font (pygame.font.Font): Font used for the button text
        rect (pygame.Rect): The button's rectangle for positioning
        msg_image (pygame.Surface): Rendered text surface
        msg_image_rect (pygame.Rect): Rectangle for the text surface
    """

    def __init__(self, ai_configuration: Configuration, screen: pygame.Surface, msg: str) -> None:
        """Initialize button attributes.

        Args:
            ai_configuration (Settings): Game configuration settings
            screen (pygame.Surface): The game screen surface
            msg (str): The text to display on the button
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Calculate button dimensions based on screen size
        base_width = 200
        base_height = 50
        scale_factor = min(ai_configuration.screen_width / 1280, ai_configuration.screen_height / 720)

        # Set the button's dimensions and properties
        self.width: int = int(base_width * scale_factor)
        self.height: int = int(base_height * scale_factor)
        self.button_color: Tuple[int, int, int] = (0, 255, 0)
        self.text_color: Tuple[int, int, int] = (255, 255, 255)
        self.font = pygame.font.SysFont(None, int(48 * scale_factor))

        # Construct the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button's message should only be set once
        self.prep_msg(msg)

    def prep_msg(self, msg: str) -> None:
        """Convert the message to a rendered image and center the text.

        Args:
            msg (str): The text to render on the button

        This method creates a rendered surface of the text and centers
        it on the button's rectangle.
        """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) -> None:
        """Draw the button and its text on the screen.

        This method is called every frame to render the button.
        It first draws the button's background color, then blits
        the text surface on top of it.
        """
        # Draw the button in white, then draw the message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
