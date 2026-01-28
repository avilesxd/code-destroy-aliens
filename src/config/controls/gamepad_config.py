"""Gamepad configuration and button mapping module.

This module manages customizable gamepad controls including:
- Button mapping configuration (save/load)
- Multiple preset configurations (Xbox, PlayStation, Custom)
- User-defined button assignments
- Persistent storage of custom mappings
"""

from __future__ import annotations

from typing import Dict, Optional

from src.core.path_utils import ensure_data_directory, load_json_file, save_json_file


class GamepadConfig:
    """Manages gamepad button mapping and configuration.

    This class handles loading, saving, and managing gamepad button mappings,
    allowing users to customize which buttons perform which actions.

    Attributes:
        config_file (str): Path to the configuration file
        mappings (Dict[str, int]): Current button mappings (action -> button number)
        current_preset (str): Name of the current preset (xbox, playstation, custom)
    """

    # Default button mappings for different controller types
    PRESETS: Dict[str, Dict[str, int]] = {
        "xbox": {
            "fire": 0,  # A button
            "quit": 1,  # B button
            "toggle_sound": 4,  # LB
            "toggle_music": 5,  # RB
            "show_controls": 6,  # Back/Select
            "pause": 7,  # Start
        },
        "playstation": {
            "fire": 1,  # X button (position 1 on PS controllers)
            "quit": 2,  # Circle button
            "toggle_sound": 4,  # L1
            "toggle_music": 5,  # R1
            "show_controls": 8,  # Share
            "pause": 9,  # Options
        },
        "nintendo": {
            "fire": 1,  # B button (Nintendo layout)
            "quit": 0,  # A button
            "toggle_sound": 4,  # L
            "toggle_music": 5,  # R
            "show_controls": 8,  # Minus
            "pause": 9,  # Plus
        },
    }

    # Action names for display
    ACTION_NAMES: Dict[str, str] = {
        "fire": "Disparar",
        "quit": "Salir",
        "toggle_sound": "Alternar Sonido",
        "toggle_music": "Alternar Música",
        "show_controls": "Mostrar Controles",
        "pause": "Pausa",
    }

    def __init__(self, preset: str = "xbox") -> None:
        """Initialize gamepad configuration.

        Args:
            preset: Initial preset to load (xbox, playstation, nintendo, or custom)
        """
        self.config_file = "gamepad_config.json"
        self.current_preset = preset
        self.mappings: Dict[str, int] = {}

        # Try to load custom configuration
        if not self._load_config():
            # If no custom config, load preset
            self.load_preset(preset)

    def load_preset(self, preset_name: str) -> bool:
        """Load a predefined button mapping preset.

        Args:
            preset_name: Name of the preset (xbox, playstation, nintendo)

        Returns:
            True if preset loaded successfully, False otherwise
        """
        if preset_name.lower() in self.PRESETS:
            self.mappings = self.PRESETS[preset_name.lower()].copy()
            self.current_preset = preset_name.lower()
            return True
        return False

    def get_button(self, action: str) -> Optional[int]:
        """Get the button number assigned to an action.

        Args:
            action: Action name (fire, quit, pause, etc.)

        Returns:
            Button number or None if action not mapped
        """
        return self.mappings.get(action)

    def set_button(self, action: str, button: int) -> None:
        """Assign a button to an action.

        Args:
            action: Action name (fire, quit, pause, etc.)
            button: Button number to assign
        """
        self.mappings[action] = button
        self.current_preset = "custom"

    def get_action_for_button(self, button: int) -> Optional[str]:
        """Get the action assigned to a button number.

        Args:
            button: Button number to check

        Returns:
            Action name or None if button not mapped
        """
        for action, btn in self.mappings.items():
            if btn == button:
                return action
        return None

    def reset_to_default(self) -> None:
        """Reset to default Xbox preset."""
        self.load_preset("xbox")

    def save_config(self) -> bool:
        """Save current configuration to file.

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            ensure_data_directory()
            config_data = {"preset": self.current_preset, "mappings": self.mappings}
            save_json_file(self.config_file, config_data)
            return True
        except Exception as e:
            print(f"Error saving gamepad config: {e}")
            return False

    def _load_config(self) -> bool:
        """Load configuration from file.

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            config_data = load_json_file(self.config_file)
            if config_data and isinstance(config_data, dict):
                self.current_preset = config_data.get("preset", "xbox")
                self.mappings = config_data.get("mappings", {})
                return True
            return False
        except Exception:
            return False

    def get_all_mappings(self) -> Dict[str, int]:
        """Get all current button mappings.

        Returns:
            Dictionary of action -> button mappings
        """
        return self.mappings.copy()

    def is_button_mapped(self, button: int) -> bool:
        """Check if a button is already mapped to an action.

        Args:
            button: Button number to check

        Returns:
            True if button is mapped, False otherwise
        """
        return button in self.mappings.values()

    def swap_buttons(self, action1: str, action2: str) -> None:
        """Swap button assignments between two actions.

        Args:
            action1: First action
            action2: Second action
        """
        if action1 in self.mappings and action2 in self.mappings:
            self.mappings[action1], self.mappings[action2] = (
                self.mappings[action2],
                self.mappings[action1],
            )
            self.current_preset = "custom"

    def get_preset_name(self) -> str:
        """Get the current preset name.

        Returns:
            Current preset name
        """
        return self.current_preset

    def get_available_presets(self) -> list[str]:
        """Get list of available presets.

        Returns:
            List of preset names
        """
        return list(self.PRESETS.keys())
