import pygame
from pygame.sprite import Sprite
from src.core.path_utils import resource_path
from src.config.music import Music


class Alien(Sprite):
    """Serves to represent a single alien in the fleet"""

    def __init__(self, ai_configuration, screen):
        """Initializes the alien and sets its initial position"""
        super(Alien, self).__init__()

        self.screen = screen
        self.ai_configuration = ai_configuration
        self.music = Music()

        # We use resource_path() to get the correct path of the alien image
        image_path = resource_path("src/assets/images/alien.png")

        # Loads the alien image and sets its rect attribute
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # Starts each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Stores the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Returns true if the alien is on the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right"""
        self.x += (
            self.ai_configuration.alien_speed_factor
            * self.ai_configuration.fleet_direction
        )
        self.rect.x = self.x

    def explode(self):
        """Play explosion sound effect"""
        self.music.play_explosion()
