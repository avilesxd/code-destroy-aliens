import pygame
from src.core.path_utils import resource_path


class Music:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Music, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize the function so the music can start playing
        pygame.mixer.init()

        # Use resource_path() to get the correct music path
        music_path = resource_path("src/assets/music/music.mp3")

        # Variable to define the music for the game
        self.sound = pygame.mixer.Sound(music_path)

        # Set the music volume
        self.sound.set_volume(0.5)

        # Load sound effects
        self.shoot_sound = pygame.mixer.Sound(resource_path("src/assets/sounds/shoot.wav"))
        self.explosion_sound = pygame.mixer.Sound(resource_path("src/assets/sounds/explosion.wav"))
        self.game_over_sound = pygame.mixer.Sound(resource_path("src/assets/sounds/game_over.wav"))

        # Set sound effects volume
        self.shoot_sound.set_volume(0.3)
        self.explosion_sound.set_volume(0.4)
        self.game_over_sound.set_volume(0.5)

        # Pass the variable with the music and add the value "-1" to play the music infinitely
        pygame.mixer.Sound.play(self.sound, -1)
        
        self._initialized = True

    def pause(self):
        """Pause the music"""
        pygame.mixer.pause()

    def resume(self):
        """Resume the music"""
        pygame.mixer.unpause()

    def play_shoot(self):
        """Play shoot sound effect"""
        self.shoot_sound.play()

    def play_explosion(self):
        """Play explosion sound effect"""
        self.explosion_sound.play()

    def play_game_over(self):
        """Play game over sound effect"""
        self.game_over_sound.play()
