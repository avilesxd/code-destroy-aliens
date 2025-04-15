import pygame.font
from pygame.sprite import Group
from src.entities.ship import Ship


class Scoreboard:
    """A class for reporting score information"""

    def __init__(self, ai_configuration, screen, statistics):
        """Initializes the score-recording attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_configuration = ai_configuration
        self.stats = statistics

        # Font setting for score information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turns the score into a rendered image"""
        redended_score = int(round(self.stats.score, -1))
        score_str = "Score: " + "{:,}".format(redended_score)
        self.image_score = self.font.render(
            score_str, True, self.text_color, self.ai_configuration.bg_color
        )

        # Display the score in the upper right corner of the screen
        self.rect_score = self.image_score.get_rect()
        self.rect_score.right = self.screen_rect.right - 20
        self.rect_score.top = 20

    def prep_high_score(self):
        """Turns the highest score into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "Maximum Score {:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_configuration.bg_color
        )

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        self.level_image = self.font.render(
            "Level: " + str(self.stats.level),
            True,
            self.text_color,
            self.ai_configuration.bg_color,
        )

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.rect_score.bottom + 10

    def prep_ships(self):
        """Display how many ships are left"""
        self.ships = Group()
        for number_ships in range(self.stats.ships_remaining):
            ship = Ship(self.ai_configuration, self.screen)
            ship.rect.x = 10 + number_ships * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw the score onscreen"""
        self.screen.blit(self.image_score, self.rect_score)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw the ships
        self.ships.draw(self.screen)
        
        # Show pause text if game is paused
        if self.stats.game_paused:
            pause_font = pygame.font.SysFont(None, 72)
            pause_image = pause_font.render("PAUSED", True, (255, 0, 0), self.ai_configuration.bg_color)
            pause_rect = pause_image.get_rect()
            pause_rect.centerx = self.screen_rect.centerx
            pause_rect.centery = self.screen_rect.centery
            self.screen.blit(pause_image, pause_rect)
