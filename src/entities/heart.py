import pygame
from pygame.sprite import Sprite
from src.core.path_utils import resource_path


class Heart(Sprite):
    """A class to represent a heart for lives display"""

    def __init__(self, screen):
        """Initialize the heart and set its starting position"""
        super(Heart, self).__init__()
        self.screen = screen

        # Load the heart image and get its rect
        image_path = resource_path("src/assets/images/heart.png")
        self.image = pygame.image.load(image_path)

        # Scale the heart to a larger size (increased from 20x20 to 30x30)
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw the heart at its current location"""
        self.screen.blit(self.image, self.rect)
