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

        # Load high score from localStorage or initialize to 0
        try:
            import json
            with open('high_score.json', 'r') as f:
                self.high_score = json.load(f)['high_score']
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0

    def reset_stats(self):
        """Initializes statistics that can change during the game"""
        self.ships_remaining = self.ai_configuration.ship_count
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """Saves the current high score to localStorage"""
        import json
        with open('high_score.json', 'w') as f:
            json.dump({'high_score': self.high_score}, f)
