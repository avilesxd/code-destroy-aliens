import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Used to handle bullets fired from the ship"""

    def __init__(self, ai_configuration, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set the correct position
        self.rect = pygame.Rect(
            0, 0, ai_configuration.bullet_width, ai_configuration.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_configuration.bullet_color
        self.velocity_factor = ai_configuration.bullets_speed_factor

    def update(self):
        """Move the bullet up on the screen"""
        # Update the bullet's decimal position
        self.y -= self.velocity_factor
        # Update the rect's position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
