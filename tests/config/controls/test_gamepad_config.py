"""Tests for gamepad configuration functionality."""

from unittest.mock import Mock, patch

import pytest

from src.config.controls.gamepad_config import GamepadConfig


class TestGamepadConfig:
    """Test suite for GamepadConfig class."""

    @patch("src.config.controls.gamepad_config.load_json_file")
    def test_init_with_xbox_preset(self, mock_load: Mock) -> None:
        """Test initialization with Xbox preset."""
        mock_load.return_value = None  # No saved config
        config = GamepadConfig(preset="xbox")

        assert config.current_preset == "xbox"
        assert config.get_button("fire") == 0
        assert config.get_button("quit") == 1
        assert config.get_button("toggle_sound") == 4

    @patch("src.config.controls.gamepad_config.load_json_file")
    def test_init_with_playstation_preset(self, mock_load: Mock) -> None:
        """Test initialization with PlayStation preset."""
        mock_load.return_value = None  # No saved config
        config = GamepadConfig(preset="playstation")

        assert config.current_preset == "playstation"
        assert config.get_button("fire") == 1
        assert config.get_button("quit") == 2

    @patch("src.config.controls.gamepad_config.load_json_file")
    def test_init_with_nintendo_preset(self, mock_load: Mock) -> None:
        """Test initialization with Nintendo preset."""
        mock_load.return_value = None  # No saved config
        config = GamepadConfig(preset="nintendo")

        assert config.current_preset == "nintendo"
        assert config.get_button("fire") == 1
        assert config.get_button("quit") == 0

    def test_load_preset(self) -> None:
        """Test loading a different preset."""
        config = GamepadConfig(preset="xbox")

        assert config.load_preset("playstation") is True
        assert config.current_preset == "playstation"
        assert config.get_button("fire") == 1

    def test_load_invalid_preset(self) -> None:
        """Test loading an invalid preset returns False."""
        config = GamepadConfig(preset="xbox")

        assert config.load_preset("invalid") is False
        assert config.current_preset == "xbox"  # Should remain unchanged

    def test_get_button(self) -> None:
        """Test getting button mapping for an action."""
        config = GamepadConfig(preset="xbox")

        assert config.get_button("fire") == 0
        assert config.get_button("pause") == 7
        assert config.get_button("nonexistent") is None

    def test_set_button(self) -> None:
        """Test setting custom button mapping."""
        config = GamepadConfig(preset="xbox")

        config.set_button("fire", 5)

        assert config.get_button("fire") == 5
        assert config.current_preset == "custom"

    def test_get_action_for_button(self) -> None:
        """Test getting action for a button number."""
        config = GamepadConfig(preset="xbox")

        assert config.get_action_for_button(0) == "fire"
        assert config.get_action_for_button(7) == "pause"
        assert config.get_action_for_button(99) is None

    def test_reset_to_default(self) -> None:
        """Test resetting to default Xbox preset."""
        config = GamepadConfig(preset="playstation")
        config.set_button("fire", 10)

        config.reset_to_default()

        assert config.current_preset == "xbox"
        assert config.get_button("fire") == 0

    def test_get_all_mappings(self) -> None:
        """Test getting all button mappings."""
        config = GamepadConfig(preset="xbox")

        mappings = config.get_all_mappings()

        assert isinstance(mappings, dict)
        assert "fire" in mappings
        assert "pause" in mappings
        assert len(mappings) == 6

    def test_is_button_mapped(self) -> None:
        """Test checking if a button is already mapped."""
        config = GamepadConfig(preset="xbox")

        assert config.is_button_mapped(0) is True  # Fire button
        assert config.is_button_mapped(99) is False

    def test_swap_buttons(self) -> None:
        """Test swapping button assignments."""
        config = GamepadConfig(preset="xbox")
        fire_button = config.get_button("fire")
        quit_button = config.get_button("quit")

        config.swap_buttons("fire", "quit")

        assert config.get_button("fire") == quit_button
        assert config.get_button("quit") == fire_button
        assert config.current_preset == "custom"

    @patch("src.config.controls.gamepad_config.load_json_file")
    def test_get_preset_name(self, mock_load: Mock) -> None:
        """Test getting current preset name."""
        mock_load.return_value = None  # No saved config
        config = GamepadConfig(preset="playstation")

        assert config.get_preset_name() == "playstation"

    def test_get_available_presets(self) -> None:
        """Test getting list of available presets."""
        config = GamepadConfig()

        presets = config.get_available_presets()

        assert "xbox" in presets
        assert "playstation" in presets
        assert "nintendo" in presets

    @patch("src.config.controls.gamepad_config.save_json_file")
    @patch("src.config.controls.gamepad_config.ensure_data_directory")
    def test_save_config(self, mock_ensure_dir: Mock, mock_save_json: Mock) -> None:
        """Test saving configuration to file."""
        config = GamepadConfig(preset="xbox")

        result = config.save_config()

        assert result is True
        mock_ensure_dir.assert_called_once()
        mock_save_json.assert_called_once()

    @patch("src.config.controls.gamepad_config.save_json_file")
    @patch("src.config.controls.gamepad_config.ensure_data_directory")
    def test_save_config_error(self, mock_ensure_dir: Mock, mock_save_json: Mock) -> None:
        """Test save config handles errors gracefully."""
        config = GamepadConfig(preset="xbox")
        mock_save_json.side_effect = Exception("Save error")

        result = config.save_config()

        assert result is False

    @patch("src.config.controls.gamepad_config.load_json_file")
    def test_load_config_success(self, mock_load_json: Mock) -> None:
        """Test loading configuration from file."""
        mock_load_json.return_value = {"preset": "playstation", "mappings": {"fire": 1, "quit": 2}}

        config = GamepadConfig(preset="xbox")

        assert config.current_preset == "playstation"
        assert config.get_button("fire") == 1

    @patch("src.config.controls.gamepad_config.load_json_file")
    def test_load_config_invalid_data(self, mock_load_json: Mock) -> None:
        """Test loading invalid config falls back to preset."""
        mock_load_json.return_value = None

        config = GamepadConfig(preset="xbox")

        assert config.current_preset == "xbox"

    @patch("src.config.controls.gamepad_config.load_json_file")
    def test_load_config_error(self, mock_load_json: Mock) -> None:
        """Test load config handles errors gracefully."""
        mock_load_json.side_effect = Exception("Load error")

        config = GamepadConfig(preset="xbox")

        # Should fall back to xbox preset
        assert config.current_preset == "xbox"
        assert config.get_button("fire") == 0
