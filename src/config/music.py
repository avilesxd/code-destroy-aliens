import pygame
from src.core.utils import resource_path


class Music:
    def __init__(self):
        # Initialize the function so the music can start playing
        pygame.mixer.init()

        # Use resource_path() to get the correct music path
        music_path = resource_path("src/assets/music/music.mp3")

        # Variable to define the music for the game
        self.sound = pygame.mixer.Sound(music_path)

        # Set the music volume
        self.sound.set_volume(0.5)

        # Pass the variable with the music and add the value "-1" to play the music infinitely
        pygame.mixer.Sound.play(self.sound, -1)

    def pause(self):
        """Pause the music"""
        pygame.mixer.pause()

    def resume(self):
        """Resume the music"""
        pygame.mixer.unpause()
