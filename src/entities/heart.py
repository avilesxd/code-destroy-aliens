import pygame
from pygame.sprite import Sprite
from src.core.utils import resource_path


class Heart(Sprite):
    """A class to represent a heart for lives display"""

    def __init__(self, screen):
        """Initialize the heart and set its starting position"""
        super(Heart, self).__init__()
        self.screen = screen

        # Load the heart image and get its rect
        image_path = resource_path("src/assets/images/heart.png")
        self.image = pygame.image.load(image_path)
        
        # Scale the heart to a smaller size (adjust these values as needed)
        self.image = pygame.transform.scale(self.image, (20, 20))
        
        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw the heart at its current location"""
        self.screen.blit(self.image, self.rect) 