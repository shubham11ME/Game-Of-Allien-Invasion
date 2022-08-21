# Upload the alien image
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent single alien in the fleet."""
    def __init__(self, ai_game):
        """Initialize the alien and set starting position."""
        super().__init__()
        self.screen = ai_game.screen
        # upload the alien image and set its rect attributes.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # start each new alien at top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien exact horizontal position.
        self.x = float(self.rect.x)
