import json
import os
import ctypes

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

        # Create .data directory if it doesn't exist
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Make the directory hidden in Windows
        if os.name == 'nt':  # Check if running on Windows
            try:
                # Set the directory as hidden using Windows API
                ctypes.windll.kernel32.SetFileAttributesW(self.data_dir, 0x02)  # 0x02 is FILE_ATTRIBUTE_HIDDEN
            except Exception:
                pass  # Silently fail if we can't set the attribute
        
        # Load high score from .data directory or initialize to 0
        try:
            high_score_path = os.path.join(self.data_dir, 'high_score.json')
            with open(high_score_path, 'r') as f:
                self.high_score = json.load(f)['high_score']
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0

    def reset_stats(self):
        """Initializes statistics that can change during the game"""
        self.ships_remaining = self.ai_configuration.ship_count
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """Saves the current high score to .data directory"""
        high_score_path = os.path.join(self.data_dir, 'high_score.json')
        with open(high_score_path, 'w') as f:
            json.dump({'high_score': self.high_score}, f)
