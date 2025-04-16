import pygame.font
from pygame.sprite import Group
from src.entities.ship import Ship
from src.entities.heart import Heart


class Scoreboard:
    """A class for reporting score information"""

    def __init__(self, ai_configuration, screen, statistics, language):
        """Initialize scoreboard attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_configuration = ai_configuration
        self.statistics = statistics
        self.language = language

        # Font settings for score information
        self.text_color = (255, 255, 255)  # White text
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Convert the score to a rendered image"""
        rounded_score = int(round(self.statistics.score, -1))
        score_str = f"{self.language.get_text('score')}: {rounded_score:,}"

        # Create text surface
        text_surface = self.font.render(score_str, True, self.text_color)

        # Create background surface
        bg_surface = pygame.Surface(
            (text_surface.get_width() + 20, text_surface.get_height() + 10)
        )
        bg_surface.fill((0, 0, 0))  # Black background
        bg_surface.set_alpha(180)  # Semi-transparent

        # Place text on background
        bg_surface.blit(text_surface, (10, 5))

        self.score_image = bg_surface
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Convert the high score to a rendered image"""
        high_score = int(round(self.statistics.high_score, -1))
        high_score_str = f"{self.language.get_text('high_score')}: {high_score:,}"

        # Create text surface
        text_surface = self.font.render(high_score_str, True, self.text_color)

        # Create background surface
        bg_surface = pygame.Surface(
            (text_surface.get_width() + 20, text_surface.get_height() + 10)
        )
        bg_surface.fill((0, 0, 0))  # Black background
        bg_surface.set_alpha(180)  # Semi-transparent

        # Place text on background
        bg_surface.blit(text_surface, (10, 5))

        self.high_score_image = bg_surface
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Convert the level to a rendered image"""
        level_str = f"{self.language.get_text('level')}: {self.statistics.level}"

        # Create text surface
        text_surface = self.font.render(level_str, True, self.text_color)

        # Create background surface
        bg_surface = pygame.Surface(
            (text_surface.get_width() + 20, text_surface.get_height() + 10)
        )
        bg_surface.fill((0, 0, 0))  # Black background
        bg_surface.set_alpha(180)  # Semi-transparent

        # Place text on background
        bg_surface.blit(text_surface, (10, 5))

        self.level_image = bg_surface
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.statistics.ships_remaining):
            ship = Heart(self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw the score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

        # If the game is paused, show pause text
        if self.statistics.game_paused:
            # Create semi-transparent background for pause screen
            pause_bg = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
            pause_bg.fill((0, 0, 0))
            pause_bg.set_alpha(128)
            self.screen.blit(pause_bg, (0, 0))

            # Pause text
            pause_font = pygame.font.SysFont(None, 72)
            pause_image = pause_font.render("PAUSED", True, (255, 0, 0))
            pause_rect = pause_image.get_rect()
            pause_rect.centerx = self.screen_rect.centerx
            pause_rect.centery = self.screen_rect.centery - 40
            self.screen.blit(pause_image, pause_rect)

            # Instruction text for resume
            instruction_font = pygame.font.SysFont(None, 36)
            instruction_image = instruction_font.render(
                self.language.get_text("press_p"), True, (255, 255, 255)
            )
            instruction_rect = instruction_image.get_rect()
            instruction_rect.centerx = self.screen_rect.centerx
            instruction_rect.centery = self.screen_rect.centery + 20
            self.screen.blit(instruction_image, instruction_rect)

            # Instruction text for quit
            quit_image = instruction_font.render(
                self.language.get_text("press_q"), True, (255, 255, 255)
            )
            quit_rect = quit_image.get_rect()
            quit_rect.centerx = self.screen_rect.centerx
            quit_rect.centery = self.screen_rect.centery + 60
            self.screen.blit(quit_image, quit_rect)
