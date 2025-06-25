from typing import Tuple

import pygame


class Configuration:
    """Used to store all game settings"""

    def __init__(self) -> None:
        """Initializes the game settings"""
        # Initialize pygame to get screen info
        pygame.init()
        info = pygame.display.Info()

        # Get the current screen resolution
        self.screen_width: int = info.current_w
        self.screen_height: int = info.current_h

        # Background configuration
        self.use_gradient_background: bool = True
        self.gradient_top_color: Tuple[int, int, int] = (5, 5, 30)  # Deep space blue
        self.gradient_bottom_color: Tuple[int, int, int] = (40, 10, 60)  # Space purple
        self.use_stars: bool = True
        self.star_count: int = 150
        self.star_color: Tuple[int, int, int] = (255, 255, 255)  # White stars
        self.bg_color: Tuple[int, int, int] = (
            20,
            20,
            40,
        )  # Fallback color if gradient is not used

        # Ship settings

        # Number of player lives
        self.ship_count: int = 3

        # Bullet settings

        # Bullet width
        self.bullet_width: int = 3
        # Bullet length
        self.bullet_height: int = 15
        # Bullet color
        self.bullet_color: Tuple[int, int, int] = (0, 255, 255)  # Cyan color for shots
        # Number of bullets
        self.bullets_allowed: int = 4

        # Alien settings

        # Speed at which aliens descend when they reach the edge of the screen
        self.fleet_drop_speed: float = 4.5
        # How fast the game accelerates
        self.acceleration_scale: float = 1.1
        # How fast the point values for aliens increase
        self.score_scale: float = 1.2

        self.initialize_dynamic_configurations()

    def initialize_dynamic_configurations(self) -> None:
        """Initializes the configuration that changes throughout the game"""
        # Ship speed
        self.ship_speed_factor: float = 2.0
        # Bullet speed
        self.bullets_speed_factor: float = 1.5
        # Alien speed
        self.alien_speed_factor: float = 1.0
        # Fleet_direction, if 1 represents right; if -1, it represents left
        self.fleet_direction: int = 1
        # Score
        self.alien_points: int = 50

    def boost_speed(self) -> None:
        """Increases speed settings and point values for aliens"""
        self.ship_speed_factor *= self.acceleration_scale
        self.bullets_speed_factor *= self.acceleration_scale
        self.alien_speed_factor *= self.acceleration_scale

        self.alien_points = int(self.alien_points * self.score_scale)
