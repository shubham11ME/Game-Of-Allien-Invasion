# 1. Creating a pygame window and responding to user input

import sys
from time import sleep

import bullet
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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

        # Create an instance to store the game statistics
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self) # instance of Ship class and the self argument represent the instance of alien invasion class. the self parameter gives access to the ship to game resources

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet() # We create a group to hold the fleet of aliens, and we call _create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """start the main loop for game"""
        while True:
            """Watch for Keyboard and mouse events"""
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() # returns a tuple containing the mouse cursor’s x- and y-coordinates, when the mouse button is clicked on play button
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score() # fix pepping the score when starting a new game.
            self.sb.prep_level() # Update the level image.
            self.sb.prep_ship() # Show how many ship left.

            # Get rid of any remaining aliens and bullets
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

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
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Resplond to bullets alien collision"""
        # Check for any bullets that have hit the alien
        # If so, get rid of bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Update the score each time an alien is shot down.
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score() # check for high score

        if not self.aliens:
            # Destroy all the existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien and find the numbers of alien in a row
        # spacing between aliens is equal to width of one alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_alien_x = available_space_x // (2*alien_width)
        # Determine the number of rows of alien that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Creating the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                # Create an alien and place it on the screen
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)  # adding alien in the alien group (self.aliens)

    def _check_fleet_edges(self):
        """Respond appropriately if an alien have reach the edge of screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet's and change the direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for the alien hiting the bottom of the screen.
        self._check_alien_bottom()

    def _check_alien_bottom(self):
        """Check if any alien have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by the alien."""
        if self.stats.ship_left > 0:
            # Decrement ships_left and update scoreboard.
            self.stats.ship_left -= 1
            self.sb.prep_ship() # Update the display of ships image when player loses a ship

            # Get rid of any remaining bullets and aliens.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()  # ship appear on the top of the background
        for bullet in self.bullets.sprites(): # the bullets.sprites returns the list of all sprites in the bullet group. To draw all the bullets to the screen, loop through sprites in bullets and call draw bullets on each one.
            bullet.draw_bullet()
        # make the alien appear on the screen
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Make the most recently drawn screen visible.
        pygame.display.flip()  # tells python to make the most recently drawn screen visible and continually updates the display to show the new position of game.

if __name__ == '__main__':
    # Make the game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
