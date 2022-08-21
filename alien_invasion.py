# 1. Creating a pygame window and responding to user input

import sys

import bullet
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """Initialize the game, create game resources"""
        pygame.init() # the pygame.init() function initializes the background settings that Pygame needs to work properly.
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # this creates a display window, on which we'll drawn all the game graphics elements. and we assign it to self.screen, so that it can be available in all methods of the class.
        # the object assign to self.screen is called 'surface'
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self) # instance of Ship class and the self argument represent the instance of alien invasion class. the self parameter gives access to the ship to game resources

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet() # We create a group to hold the fleet of aliens, and we call _create_fleet()

    def run_game(self):
        """start the main loop for game"""
        while True:
            """Watch for Keyboard and mouse events"""
            self._check_events()
            self.ship.update()
            self._update_bullets()
            print(len(self.bullets))
            self._update_screen() # Redrawn the screen during each pass through the loop.

    def _check_events(self):
        """Response to keypresses and mouse events"""
        for event in pygame.event.get():  # an event is an action that a player perform while playing the game.
            # pygame.event.get() returns a list of events that have taken place, since the last time this function was called.
            if event.type == pygame.QUIT:
                sys.exit()
            # Moving ship to the Right on the screen.
            elif event.type == pygame.KEYDOWN:
                self._check_Keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_Keydown_events(self, event):
        """Respond to Key-presses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        # To Quit the game
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # fire the bullet when the spacebar is pressed.

    def _check_keyup_events(self, event):
        """Respond to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self) # new_bullet is teh Instance of Bullet class
            self.bullets.add(new_bullet) # add new bullets to the group bullets using add() method

    def _update_bullets(self):
        """Update the bullets and get rid of old bullets."""
        # Update bullet position
        self.bullets.update()  # update the position of bullets on each pass. the line self.bullet.update() calls bullet.update for each bullet we place in the group
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():  # because we don't want to remove items from list so we work with copy of list
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien and find the numbers of alien in a row
        # spacing between aliens is equal to width of one alien
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_alien_x = available_space_x // (2*alien_width)
        # Creating the first row of alien
        for alien_number in range(number_alien_x):
            # Create an alien and place it on the screen
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien) # adding alien in the alien group (self.aliens)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()  # ship appear on the top of the background
        for bullet in self.bullets.sprites(): # the bullets.sprites returns the list of all sprites in the bullet group. To draw all the bullets to the screen, loop through sprites in bullets and call draw bullets on each one.
            bullet.draw_bullet()
        # make the alien appear on the screen
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()  # tells python to make the most recently drawn screen visible and continually updates the display to show the new position of game.

if __name__ == '__main__':
    # Make the game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
