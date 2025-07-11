import pygame
from pygame.sprite import Sprite

from src.config.configuration import Configuration
from src.config.music.music import Music
from src.config.statistics.statistics import Statistics
from src.core.path_utils import resource_path


class Ship(Sprite):
    """A class to manage the player's ship in the game.

    This class handles the ship's movement, shooting, and rendering.
    It inherits from pygame.sprite.Sprite to enable sprite-based
    collision detection and rendering.

    Attributes:
        screen (pygame.Surface): The game screen surface
        screen_rect (pygame.Rect): The screen's rectangle
        image (pygame.Surface): The ship's image
        rect (pygame.Rect): The ship's rectangle for positioning
        center (float): The ship's center x-coordinate
        music (Music): Sound effects manager
    """

    def __init__(
        self,
        ai_configuration: Configuration,
        screen: pygame.Surface,
        statistics: Statistics,
        music: Music,
    ) -> None:
        """Initialize the ship and set its starting position.

        Args:
            ai_configuration (Settings): Game configuration settings
            screen (pygame.Surface): The game screen surface
            statistics (Statistics): Game statistics manager
        """
        super().__init__()
        self.screen = screen
        self.ai_configuration = ai_configuration
        self.statistics = statistics

        # Load the ship image and get its rect
        self.image = pygame.image.load(resource_path("src/assets/images/ship.png"))

        # Calculate scale factor based on screen resolution
        scale_factor = min(ai_configuration.screen_width / 1280, ai_configuration.screen_height / 720)
        original_size = self.image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = pygame.transform.scale(self.image, new_size)

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

        # Initialize music object
        self.music = music

    def update(self) -> None:
        """Update the ship's position based on movement flags.

        This method is called every frame to update the ship's position.
        It checks the movement flags and moves the ship accordingly,
        ensuring it stays within the screen boundaries.
        """
        # Don't move if the game is paused
        if self.statistics and self.statistics.game_paused:
            return

        # Calculate new position
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_configuration.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_configuration.ship_speed_factor

        # Update rect position
        self.rect.centerx = int(self.center)

    def blitme(self) -> None:
        """Draw the ship at its current location.

        This method is called every frame to render the ship
        at its current position on the screen.
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self) -> None:
        """Center the ship on the screen.

        This method is called when a new ship is created or
        when the game is reset.
        """
        self.center = float(self.screen_rect.centerx)
        self.rect.centerx = int(self.center)

    def shoot(self) -> None:
        """Play the shooting sound effect.

        This method is called whenever the player fires a bullet.
        """
        self.music.play_shoot()
