import pygame
from pygame.sprite import Sprite # group related elements in game and act on grouped elements at once.

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_game):
        """Create a bullet object at the ship current position."""
        super().__init__() # Inherit properly form sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) # pygame.Rect() creates a rect from scratch and it requires the top left coordinates of rect
        self.rect.midtop = ai_game.ship.rect.midtop # Move bullets to the the mid position because bullet position depend on the ship position.

        # Store the bullet position as decimal value.
        self.y = float(self.rect.y)

    def update(self): # Update method manage the bullet position.
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed # when a bullet is fired, it's moves up the screen, which correspond to decreasing value of y.
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect) # the draw.rect() function fill the part with screen defined by bullet.rect with color stored in self.color
