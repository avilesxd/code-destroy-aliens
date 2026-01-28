"""Gamepad configuration screen.

This module provides a user interface for configuring gamepad controls,
allowing players to customize button mappings and choose between presets.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pygame

if TYPE_CHECKING:
    from src.config.configuration import Configuration
    from src.config.controls.gamepad_config import GamepadConfig
    from src.config.language.language import Language


class GamepadConfigScreen:
    """Screen for configuring gamepad button mappings.

    Provides an interactive UI for:
    - Selecting controller presets (Xbox, PlayStation, Nintendo)
    - Customizing individual button mappings
    - Testing button assignments
    - Saving/loading configurations

    Attributes:
        screen (pygame.Surface): The game screen
        config (GamepadConfig): Gamepad configuration manager
        font (pygame.font.Font): Font for regular text
        title_font (pygame.font.Font): Font for titles
        selected_action (Optional[str]): Currently selected action for remapping
        waiting_for_button (bool): Whether waiting for button press to remap
    """

    def __init__(
        self,
        ai_configuration: Configuration,
        screen: pygame.Surface,
        gamepad_config: GamepadConfig,
        language: Language,
    ) -> None:
        """Initialize the gamepad configuration screen.

        Args:
            ai_configuration: Game configuration
            screen: Pygame screen surface
            gamepad_config: Gamepad configuration manager
            language: Language manager for translations
        """
        self.screen = screen
        self.config = gamepad_config
        self.language = language
        self.ai_configuration = ai_configuration

        # Fonts
        self.title_font = pygame.font.SysFont(None, 64)
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)

        # Colors
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 255, 255)
        self.text_color = (200, 200, 200)
        self.selected_color = (0, 255, 255)
        self.button_color = (255, 200, 0)

        # State
        self.selected_action: Optional[str] = None
        self.waiting_for_button = False
        self.selected_preset_index = 0
        self.selected_action_index = 0

        # Get available presets and actions
        self.presets = self.config.get_available_presets()
        self.actions = list(self.config.ACTION_NAMES.keys())

    def draw(self) -> None:
        """Draw the gamepad configuration screen."""
        self.screen.fill(self.bg_color)

        # Title
        title_text = "Configuración de Gamepad"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_surface, title_rect)

        # Current preset
        preset_text = f"Preset: {self.config.get_preset_name().upper()}"
        preset_surface = self.font.render(preset_text, True, self.text_color)
        preset_rect = preset_surface.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(preset_surface, preset_rect)

        # Draw preset selection
        y_offset = 180
        for i, preset in enumerate(self.presets):
            color = self.selected_color if i == self.selected_preset_index else self.text_color
            preset_display = f"[{i + 1}] {preset.upper()}"
            preset_surf = self.font.render(preset_display, True, color)
            preset_rect = preset_surf.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(preset_surf, preset_rect)
            y_offset += 40

        # Draw button mappings
        y_offset += 20
        mappings_title = self.font.render("Mapeo de Botones:", True, self.title_color)
        mappings_rect = mappings_title.get_rect(center=(self.screen.get_width() // 2, y_offset))
        self.screen.blit(mappings_title, mappings_rect)
        y_offset += 50

        # Draw each action and its button
        for i, action in enumerate(self.actions):
            action_name = self.config.ACTION_NAMES.get(action, action)
            button = self.config.get_button(action)

            # Highlight selected action
            color = self.selected_color if i == self.selected_action_index else self.text_color

            if button is not None:
                text = f"{action_name}: Botón {button}"
            else:
                text = f"{action_name}: No asignado"

            action_surface = self.font.render(text, True, color)
            action_rect = action_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(action_surface, action_rect)
            y_offset += 40

        # Instructions
        y_offset += 30
        if self.waiting_for_button:
            instruction = "Presiona un botón en tu gamepad..."
            instruction_color = self.button_color
        else:
            instruction = "↑↓: Seleccionar | Enter: Cambiar | ESC: Guardar y Salir"
            instruction_color = self.text_color

        instruction_surface = self.small_font.render(instruction, True, instruction_color)
        instruction_rect = instruction_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
        self.screen.blit(instruction_surface, instruction_rect)

        # Additional instructions
        y_offset += 40
        save_text = "S: Guardar | R: Resetear a defaults"
        save_surface = self.small_font.render(save_text, True, self.text_color)
        save_rect = save_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
        self.screen.blit(save_surface, save_rect)

    def handle_keyboard_input(self, event: pygame.event.Event) -> bool:
        """Handle keyboard input for the configuration screen.

        Args:
            event: Pygame keyboard event

        Returns:
            True if should close the config screen, False otherwise
        """
        if event.type != pygame.KEYDOWN:
            return False

        # Close screen with ESC
        if event.key == pygame.K_ESCAPE:
            self.config.save_config()
            return True

        # Save configuration
        if event.key == pygame.K_s:
            self.config.save_config()
            return False

        # Reset to default
        if event.key == pygame.K_r:
            self.config.reset_to_default()
            return False

        # Navigate presets with number keys
        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
            preset_index = event.key - pygame.K_1
            if preset_index < len(self.presets):
                self.config.load_preset(self.presets[preset_index])
                self.selected_preset_index = preset_index
            return False

        # Navigate actions
        if event.key == pygame.K_UP:
            self.selected_action_index = (self.selected_action_index - 1) % len(self.actions)
            return False

        if event.key == pygame.K_DOWN:
            self.selected_action_index = (self.selected_action_index + 1) % len(self.actions)
            return False

        # Start remapping
        if event.key == pygame.K_RETURN:
            self.selected_action = self.actions[self.selected_action_index]
            self.waiting_for_button = True
            return False

        return False

    def handle_gamepad_input(self, event: pygame.event.Event) -> None:
        """Handle gamepad input for button remapping.

        Args:
            event: Pygame joystick button event
        """
        if event.type == pygame.JOYBUTTONDOWN and self.waiting_for_button and self.selected_action:
            # Assign button to selected action
            self.config.set_button(self.selected_action, event.button)
            self.waiting_for_button = False
            self.selected_action = None
