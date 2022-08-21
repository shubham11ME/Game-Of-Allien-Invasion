# upload the ship image
import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game): # ai_game is the current instance of AlienInvasion class. This give access to the Ship to all the game resources used in alien invasion class.
        """Initialize the ship and starting position"""
        self.screen = ai_game.screen
        # create a setting attribute, so we can use it in update()
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() # this place the ship in the correct position on the screen

        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp') # this functon returns the surface representing the ship
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for ship horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship position based on the movement flag"""
        # Update the ship x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right: # self.rect.right returns the x- coordinates of right edge of ship's rect.
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Update rect object form self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
