import json
import os
import ctypes
import sys
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.core.path_utils import get_app_directory, ensure_data_directory, load_json_file, save_json_file, resource_path
from src.config.music import Music


class Statistics:
    """Alien Invasion stats tracker"""

    # Encryption key derived from a fixed password (this is not secure for real applications,
    # but it's enough to prevent casual edits by players)
    _SALT = b'code-destroy-aliens-salt'
    _PASSWORD = b'code-destroy-aliens-password'
    
    @classmethod
    def _get_encryption_key(cls):
        """Generates an encryption key from the password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=cls._SALT,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(cls._PASSWORD))
        return Fernet(key)
    
    @classmethod
    def _encrypt_data(cls, data):
        """Encrypts JSON data"""
        json_data = json.dumps(data)
        fernet = cls._get_encryption_key()
        encrypted_data = fernet.encrypt(json_data.encode())
        
        # Add a verification hash
        data_hash = hashlib.sha256(json_data.encode()).hexdigest()
        return encrypted_data, data_hash
    
    @classmethod
    def _decrypt_data(cls, encrypted_data, stored_hash):
        """Decrypts JSON data and verifies its integrity"""
        try:
            fernet = cls._get_encryption_key()
            decrypted_data = fernet.decrypt(encrypted_data)
            json_data = decrypted_data.decode()
            
            # Verify the hash
            data_hash = hashlib.sha256(json_data.encode()).hexdigest()
            if data_hash != stored_hash:
                # If the hash doesn't match, the data has been tampered with
                return None
            
            return json.loads(json_data)
        except Exception:
            # If there's any error in decryption, return None
            return None

    def __init__(self, ai_configuration):
        """Initializes statistics"""
        self.ai_configuration = ai_configuration
        self.music = Music()
        
        # Game state flags
        self.game_active = False
        self.game_paused = False
        self.game_over = False
        self.show_controls = True
        self.controls_seen = False  # Initialize controls_seen first

        # Get the data directory and ensure it exists
        self.data_dir = ensure_data_directory()

        # Load high score from .data directory or initialize to 0
        self.load_high_score()
        
        # Initialize the rest of the stats
        self.reset_stats()

    def reset_stats(self):
        """Initializes statistics that can change during the game"""
        self.ships_remaining = self.ai_configuration.ship_count
        self.score = 0
        self.level = 1
        self.aliens_destroyed = 0
        self.bullets_fired = 0
        self.game_over = False
        # Only show controls if they haven't been seen before
        self.show_controls = not self.controls_seen

    def save_high_score(self):
        """Saves the current high score to .data directory"""
        data = {
            'high_score': self.high_score,
            'hash': None  # Will be updated later
        }
        
        # Encrypt the data
        encrypted_data, data_hash = self._encrypt_data({'high_score': self.high_score})
        
        # Save the encrypted data and hash
        file_path = os.path.join(self.data_dir, 'high_score.dat')
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
            f.write(b'\n')  # Separator
            f.write(data_hash.encode())

    def load_high_score(self):
        """Load high score from a file"""
        file_path = os.path.join(self.data_dir, 'high_score.dat')
        self.high_score = 0
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    # Separate the encrypted data from the hash
                    parts = content.split(b'\n')
                    if len(parts) == 2:
                        encrypted_data, stored_hash = parts
                        # Decrypt and verify the data
                        data = self._decrypt_data(encrypted_data, stored_hash.decode())
                        if data and 'high_score' in data:
                            self.high_score = data['high_score']
            except Exception:
                # If there's an error, use the default value
                self.high_score = 0

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
        self.music.play_game_over()

    def start_game(self):
        """Starts a new game"""
        self.reset_stats()
        self.game_active = True
        self.game_paused = False
        self.game_over = False
