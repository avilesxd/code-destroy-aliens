from typing import Dict, Optional, Tuple

import pygame

from src.core.path_utils import resource_path


class ResourceManager:
    """Singleton class to manage game resources (images, sounds).

    This manager caches loaded resources to avoid redundant disk access
    and optimizes surfaces for faster rendering.
    """

    _instance: Optional["ResourceManager"] = None
    _images: Dict[str, pygame.Surface]
    _scaled_images: Dict[Tuple[str, Tuple[int, int]], pygame.Surface]
    _sounds: Dict[str, pygame.mixer.Sound]

    def __new__(cls) -> "ResourceManager":
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._images = {}
            instance._scaled_images = {}
            instance._sounds = {}
            cls._instance = instance
        return cls._instance

    def get_image(self, path: str, scale: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        """Load, optimize, and cache an image.

        Args:
            path: Relative path to the image asset.
            scale: Optional (width, height) tuple to scale the image.

        Returns:
            A pygame Surface optimized for the current display.
        """
        full_path = resource_path(path)

        if scale:
            cache_key = (full_path, scale)
            if cache_key in self._scaled_images:
                return self._scaled_images[cache_key]

            base_image = self._get_base_image(full_path)
            scaled_image = pygame.transform.scale(base_image, scale)
            self._scaled_images[cache_key] = scaled_image
            return scaled_image

        return self._get_base_image(full_path)

    def _get_base_image(self, full_path: str) -> pygame.Surface:
        """Internal helper to load and optimize base images."""
        if full_path not in self._images:
            image = pygame.image.load(full_path)
            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
            self._images[full_path] = image
        return self._images[full_path]

    def get_sound(self, path: str) -> pygame.mixer.Sound:
        """Load and cache a sound effect."""
        full_path = resource_path(path)
        if full_path not in self._sounds:
            self._sounds[full_path] = pygame.mixer.Sound(full_path)
        return self._sounds[full_path]

    def clear_cache(self) -> None:
        """Clear all cached resources."""
        self._images.clear()
        self._scaled_images.clear()
        self._sounds.clear()
