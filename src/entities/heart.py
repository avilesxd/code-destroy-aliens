from typing import Optional

import pygame
from pygame.sprite import Sprite

from src.config.configuration import Configuration
from src.core.path_utils import resource_path


class Heart(Sprite):
    """A class to represent a heart for lives display"""

    def __init__(self, screen: pygame.Surface, ai_configuration: Optional[Configuration] = None) -> None:
        """Initialize the heart and set its starting position"""
        super().__init__()
        self.screen = screen

        # Load the heart image and get its rect
        image_path = resource_path("src/assets/images/heart.png")
        self.image = pygame.image.load(image_path)

        # Calculate scale factor based on screen resolution
        if ai_configuration:
            scale_factor = min(ai_configuration.screen_width / 1280, ai_configuration.screen_height / 720)
        else:
            # Default scale factor if no configuration is provided
            scale_factor = 1.0

        # Scale the heart based on screen resolution
        base_size = 30  # Base size for 1280x720 resolution
        new_size = int(base_size * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_size, new_size))

        self.rect = self.image.get_rect()

    def blitme(self) -> None:
        """Draw the heart at its current location"""
        self.screen.blit(self.image, self.rect)
