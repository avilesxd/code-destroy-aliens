import os
from typing import Any, Optional, Union

import pygame
from pygame.mixer import Sound

from src.core.path_utils import resource_path


class DummySound:
    def play(self, *args: Any) -> None:
        pass

    def get_volume(self) -> float:
        return 0.0

    def set_volume(self, value: float) -> None:
        pass


SoundType = Union[Sound, DummySound]


class Music:
    _instance: Optional["Music"] = None
    _initialized: bool

    def __new__(cls: type["Music"]) -> "Music":
        if cls._instance is None:
            cls._instance = super(Music, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        # Check if we're in a test environment
        self.is_test: bool = "PYTEST_CURRENT_TEST" in os.environ

        try:
            # Initialize the function so the music can start playing
            pygame.mixer.init()

            # Use resource_path() to get the correct music path
            music_path = resource_path("src/assets/music/music.mp3")

            # Variable to define the music for the game
            self.sound: SoundType = pygame.mixer.Sound(music_path)

            # Set the music volume
            self.sound.set_volume(0.5)

            # Load sound effects
            self.shoot_sound: SoundType = pygame.mixer.Sound(
                resource_path("src/assets/sounds/shoot.wav")
            )
            self.explosion_sound: SoundType = pygame.mixer.Sound(
                resource_path("src/assets/sounds/explosion.wav")
            )
            self.game_over_sound: SoundType = pygame.mixer.Sound(
                resource_path("src/assets/sounds/game_over.wav")
            )

            # Set sound effects volume
            self.shoot_sound.set_volume(0.3)
            self.explosion_sound.set_volume(0.4)
            self.game_over_sound.set_volume(0.5)

            # Pass the variable with the music and add the value "-1" to play the music infinitely
            if not self.is_test:
                pygame.mixer.Sound.play(self.sound, -1)
        except pygame.error:
            self.sound = DummySound()
            self.shoot_sound = DummySound()
            self.explosion_sound = DummySound()
            self.game_over_sound = DummySound()

        self._initialized = True

    @property
    def volume(self) -> float:
        """Get the current volume of the main sound"""
        return self.sound.get_volume()

    @volume.setter
    def volume(self, value: float) -> None:
        """Set the volume of the main sound"""
        self.sound.set_volume(value)

    def pause(self) -> None:
        """Pause the music"""
        if not self.is_test:
            pygame.mixer.pause()

    def resume(self) -> None:
        """Resume the music"""
        if not self.is_test:
            pygame.mixer.unpause()

    def play_shoot(self) -> None:
        """Play shoot sound effect"""
        if not self.is_test:
            self.shoot_sound.play()

    def play_explosion(self) -> None:
        """Play explosion sound effect"""
        if not self.is_test:
            self.explosion_sound.play()

    def play_game_over(self) -> None:
        """Play game over sound effect"""
        if not self.is_test:
            # Pause the background music
            pygame.mixer.pause()
            # Increase volume for game over sound
            self.game_over_sound.set_volume(1.0)
            # Play the game over sound
            self.game_over_sound.play()
