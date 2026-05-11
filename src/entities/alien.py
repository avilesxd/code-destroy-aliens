import pygame
from pygame.sprite import Sprite

from src.config.configuration import Configuration
from src.config.music.music import Music
from src.core.resource_manager import ResourceManager


class Alien(Sprite):
    """Serves to represent a single alien in the fleet"""

    def __init__(self, ai_configuration: Configuration, screen: pygame.Surface) -> None:
        """Initializes the alien and sets its initial position"""
        super().__init__()

        self.screen = screen
        self.ai_configuration = ai_configuration
        self.music = Music()
        self.resource_manager = ResourceManager()

        # Calculate scale factor based on screen resolution
        scale_factor = min(ai_configuration.screen_width / 1280, ai_configuration.screen_height / 720)

        # Load the alien image through ResourceManager
        base_img = self.resource_manager.get_image("src/assets/images/alien.png")
        original_size = base_img.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = self.resource_manager.get_image("src/assets/images/alien.png", scale=new_size)

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

    def update_image(self) -> None:
        """Update the alien's image based on current configuration (e.g., after a resize)."""
        scale_factor = min(self.ai_configuration.screen_width / 1280, self.ai_configuration.screen_height / 720)
        base_img = self.resource_manager.get_image("src/assets/images/alien.png")
        original_size = base_img.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = self.resource_manager.get_image("src/assets/images/alien.png", scale=new_size)

        # Preserve position
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
