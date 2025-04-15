class Configuration:
    """Used to store all game settings"""

    def __init__(self):
        """Initializes the game settings"""
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Ship settings

        # Number of player lives
        self.ship_count = 3

        # Bullet settings

        # Bullet width
        self.bullet_width = 3
        # Bullet length
        self.bullet_height = 15
        # Bullet color
        self.bullet_color = 60, 60, 60
        # Number of bullets
        self.bullets_allowed = 4

        # Alien settings

        # Speed ​​at which aliens descend when they reach the edge of the screen
        self.fleet_drop_speed = 10
        # How fast the game accelerates
        self.acceleration_scale = 1.1
        # How fast the point values ​​for aliens increase
        self.score_scale = 1.5

        self.initialize_dynamic_configurations()

    def initialize_dynamic_configurations(self):
        """Initializes the configuration that changes throughout the game"""
        # Ship speed
        self.ship_speed_factor = 1
        # Bullet speed
        self.bullets_speed_factor = 0.5
        # Alien speed
        self.alien_speed_factor = 0.5
        # Fleet_direction, if 1 represents right; if -1, it represents left
        self.fleet_direction = 1
        # Score
        self.alien_points = 50

    def boost_speed(self):
        """Increases speed settings and point values for aliens"""
        self.ship_speed_factor *= self.acceleration_scale
        self.bullets_speed_factor *= self.acceleration_scale
        self.alien_speed_factor *= self.acceleration_scale

        self.alien_points = int(self.alien_points * self.score_scale)
