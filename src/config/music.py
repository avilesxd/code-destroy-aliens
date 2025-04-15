import pygame
from src.core.utils import resource_path


def Music():
    # Initialize the function so the music can start playing
    pygame.mixer.init()

    # Use resource_path() to get the correct music path
    music_path = resource_path("src/assets/music/music.mp3")

    # Variable to define the music for the game
    sound = pygame.mixer.Sound(music_path)

    # Set the music volume
    sound.set_volume(0.5)

    # Pass the variable with the music and add the value "-1" to play the music infinitely
    pygame.mixer.Sound.play(sound, -1)
