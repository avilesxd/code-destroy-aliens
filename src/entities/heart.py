from typing import Optional

import pygame
from pygame.sprite import Sprite

from src.config.configuration import Configuration
from src.core.resource_manager import ResourceManager


class Heart(Sprite):
    """A class to represent a heart for lives display"""

    def __init__(self, screen: pygame.Surface, ai_configuration: Optional[Configuration] = None) -> None:
        """Initialize the heart and set its starting position"""
        super().__init__()
        self.screen = screen
        self.resource_manager = ResourceManager()

        # Calculate scale factor based on screen resolution
        if ai_configuration:
            scale_factor = min(ai_configuration.screen_width / 1280, ai_configuration.screen_height / 720)
        else:
            # Default scale factor if no configuration is provided
            scale_factor = 1.0

        # Scale the heart based on screen resolution
        base_size = 30  # Base size for 1280x720 resolution
        new_size_val = int(base_size * scale_factor)
        new_size = (new_size_val, new_size_val)

        # Load the heart image through ResourceManager
        self.image = self.resource_manager.get_image("src/assets/images/heart.png", scale=new_size)

        self.rect = self.image.get_rect()

    def blitme(self) -> None:
        """Draw the heart at its current location"""
        self.screen.blit(self.image, self.rect)
