import pygame
from pygame.sprite import Sprite

from src.config.configuration import Configuration
from src.config.music import Music
from src.core.path_utils import resource_path


class Alien(Sprite):
    """Serves to represent a single alien in the fleet"""

    def __init__(self, ai_configuration: Configuration, screen: pygame.Surface) -> None:
        """Initializes the alien and sets its initial position"""
        super().__init__()

        self.screen = screen
        self.ai_configuration = ai_configuration
        self.music = Music()

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load(resource_path("src/assets/images/alien.png"))

        # Calculate scale factor based on screen resolution
        scale_factor = min(ai_configuration.screen_width / 1280, ai_configuration.screen_height / 720)
        original_size = self.image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = pygame.transform.scale(self.image, new_size)

        self.rect = self.image.get_rect()

        # Starts each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Stores the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self) -> None:
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self) -> bool:
        """Returns true if the alien is on the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False

    def update(self) -> None:
        """Move the alien to the right"""
        speed_factor = self.ai_configuration.alien_speed_factor
        speed = speed_factor * self.ai_configuration.fleet_direction
        self.x += speed
        self.rect.x = int(self.x)

    def explode(self) -> None:
        """Play explosion sound effect"""
        self.music.play_explosion()
