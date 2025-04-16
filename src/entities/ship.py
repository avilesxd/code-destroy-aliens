import pygame
from pygame.sprite import Sprite
from src.core.path_utils import resource_path
from src.config.music import Music


class Ship(Sprite):
    """Used to manage the ship's behavior"""

    def __init__(self, ai_configuration, screen):
        """Initializes the ship and sets its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_configuration = ai_configuration
        self.music = Music()

        # Use resource_path() to get the correct path of the ship image
        image_path = resource_path("src/assets/images/ship.png")

        # Load the ship image and get its rect (rectangle)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each New ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Stores a decimal value for the center of the ship
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updates the ship's position based on the movement flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_configuration.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_configuration.ship_speed_factor

        # Updates the rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draws the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centers the ship on the screen"""
        self.center = self.screen_rect.centerx

    def shoot(self):
        """Play shoot sound effect"""
        self.music.play_shoot()
