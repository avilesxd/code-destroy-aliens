import json
import os
import ctypes
import sys
from src.core.path_utils import get_app_directory, ensure_data_directory, load_json_file, save_json_file


class Statistics:
    """Alien Invasion stats tracker"""

    def __init__(self, ai_configuration):
        """Initializes statistics"""
        self.ai_configuration = ai_configuration
        self.reset_stats()

        # Game state flags
        self.game_active = False
        self.game_paused = False
        self.game_over = False

        # Get the data directory and ensure it exists
        self.data_dir = ensure_data_directory()

        # Load high score from .data directory or initialize to 0
        high_score_path = os.path.join(self.data_dir, "high_score.json")
        data = load_json_file(high_score_path, {"high_score": 0})
        self.high_score = data["high_score"]

    def reset_stats(self):
        """Initializes statistics that can change during the game"""
        self.ships_remaining = self.ai_configuration.ship_count
        self.score = 0
        self.level = 1
        self.aliens_destroyed = 0
        self.bullets_fired = 0
        self.game_over = False

    def save_high_score(self):
        """Saves the current high score to .data directory"""
        try:
            high_score_path = os.path.join(self.data_dir, "high_score.json")
            save_json_file(high_score_path, {"high_score": self.high_score})
        except Exception as e:
            print(f"Error saving high score: {e}")

    def toggle_pause(self):
        """Toggles the game pause state"""
        self.game_paused = not self.game_paused
        return self.game_paused

    def end_game(self):
        """Ends the current game"""
        self.game_active = False
        self.game_paused = False
        self.game_over = True
        self.save_high_score()

    def start_game(self):
        """Starts a new game"""
        self.reset_stats()
        self.game_active = True
        self.game_paused = False
        self.game_over = False
