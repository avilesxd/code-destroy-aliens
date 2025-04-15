class Statistics:
    """Alien Invasion stats tracker"""

    def __init__(self, ai_configuration):
        """Initializes statistics"""
        self.ai_configuration = ai_configuration
        self.reset_stats()

        # Starts Alien Invasion in an active state
        self.game_active = False
        
        # Game pause state
        self.game_paused = False

        # The high score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initializes statistics that can change during the game"""
        self.ships_remaining = self.ai_configuration.ship_count
        self.score = 0
        self.level = 1
