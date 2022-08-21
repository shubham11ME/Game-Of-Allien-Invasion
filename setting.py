# 3. create setting class
class Settings:
    """A class for store all setting for the Alien Invasion."""

    def __init__(self):
        """Initialize the game setting."""
        # Screen setting
        self.screen_width = 1280
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship setting
        self.ship_speed = 1.5

        # Bullets Setting
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3