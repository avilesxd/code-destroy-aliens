from typing import List

import pygame
from pygame.sprite import Sprite

from src.config.configuration import Configuration
from src.entities.ship import Ship


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    # Class variable to store the bullet pool
    _bullet_pool: List["Bullet"] = []
    _max_pool_size: int = 100  # Maximum number of bullets to keep in the pool

    @classmethod
    def get_bullet(
        cls, ai_configuration: Configuration, screen: pygame.Surface, ship: Ship
    ) -> "Bullet":
        """Get a bullet from the pool or create a new one if pool is empty"""
        if cls._bullet_pool:
            bullet = cls._bullet_pool.pop()
            bullet.reset(ai_configuration, screen, ship)
            return bullet
        return cls(ai_configuration, screen, ship)

    @classmethod
    def return_to_pool(cls, bullet: "Bullet") -> None:
        """Return a bullet to the pool"""
        if len(cls._bullet_pool) < cls._max_pool_size:
            cls._bullet_pool.append(bullet)

    def __init__(
        self, ai_configuration: Configuration, screen: pygame.Surface, ship: Ship
    ) -> None:
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(
            0, 0, ai_configuration.bullet_width, ai_configuration.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

        self.color = ai_configuration.bullet_color
        self.speed_factor = ai_configuration.bullets_speed_factor

        # Flag to indicate if bullet is active
        self.active = True

    def reset(
        self, ai_configuration: Configuration, screen: pygame.Surface, ship: Ship
    ) -> None:
        """Reset bullet to initial state"""
        self.screen = screen
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_configuration.bullet_color
        self.speed_factor = ai_configuration.bullets_speed_factor
        self.active = True

    def update(self) -> None:
        """Move the bullet up the screen"""
        # Update the float position of the bullet
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = int(self.y)  # Convert float to int for rect position

        # If bullet goes off screen, return it to pool
        if self.rect.bottom <= 0:
            self.active = False
            Bullet.return_to_pool(self)

    def draw_bullet(self) -> None:
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
