import pygame
from typing import TYPE_CHECKING
from alien import Alien
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion



class AlienFleet:
    """A class operating the fleet of aliens as a group
    """
    def __init__(self, game:'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
        """contains multiple methods that builds the group of enemy aliens
        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calc_offsets(alien_w, alien_h, screen_w,screen_h, fleet_w, fleet_h)
        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """creates aliens in a rectangular formation with one alien gap horizontal and vertical between each

        Args:
            alien_w (Int): how wide the alien sprite is
            alien_h (Int): how tall the alien sprite is
            fleet_w (Int): how many aliens wide the fleet is
            fleet_h (Int): how many aliens tall the fleet is
            x_offset (Int): offset in the horizontal direction on each side of the fleet
            y_offset (Int): offset in the vertical direction from the top and middle of the screen
        """
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w *col + x_offset
                current_y = alien_h *row +y_offset
                if col % 2==0 or row % 2 ==0:
                    continue
                self._create_alien(current_x , current_y)

    def calc_offsets(self, alien_w, alien_h, screen_w, screen_h, fleet_w, fleet_h):
        """calculates the offset required to horizontaly center the fleet and verticaly in the top half of the screen.

        Args:
            alien_w (Int): how wide the alien sprite is
            alien_h (Int): how tall the alien sprite is
            screen_w (Int): how wide the screen is
            screen_h (Int): how tall the screen is
            fleet_w (Int): how many aliens wide the fleet is
            fleet_h (Int): how many aliens tall the fleet is
    

        Returns:
            Tuple: The x and y offset required for the fleet to be centered in the top half of screen
        """
        half_screen = screen_h // 2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h
        x_offset = int((screen_w-fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """finds dimensions of the fleet in terms of the number of aliens 

        Args:
            alien_w (int): how wide the alien sprite is
            screen_w (int): how wide the screen is
            alien_h (int): how tall the alien sprite is
            screen_h (int): how tall the screen is

        Returns:
            tuple: (the number of aliens wide the fleet can be, the number of aliens tall the fleet can be)
        """
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h /2)//alien_h)
        if fleet_w %2 == 0:
            fleet_w -= 1
        else:
            fleet_w -=2

        if fleet_h % 2 ==0:
            fleet_h -=1
        else:
            fleet_h -=2
        
        
        return int(fleet_w), int(fleet_h)


    def _create_alien(self, current_x:int , current_y:int):
        """creates an alien and adds it to the fleet at a given location

        Args:
            current_x (int): distance from the left of the screen
            current_y (int): distance from the top of the screen
        """

        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """moves the fleet down and changes direction if at least one alien is at the edge of the screen
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
                
    def _drop_alien_fleet(self):
        """drops the alien fleet down
        """
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def update_fleet(self):
        """updates the fleet by checking for one on the edge and then moves every alien
        """
        self._check_fleet_edges()
        self.fleet.update()


    def draw(self):
        """draws all aliens in the fleet
        """
        alien: Alien
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """checks if any member of the fleet is colliding with sprite from a different group and deletes both

        Args:
            other_group (group): the group of sprites that is colliding with the aliens

        Returns:
            dictionary: returns all the sprites colided and were destroyed
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_bottom(self):
        """checks if the fleet has reached the bottom of the screen

        Returns:
            Bool: True if at least one alien is at the bottom of the screen
        """
        alien:Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False

    def check_destroyed_status(self):
        """checks if there are any aliens left in the fleet

        Returns:
            Bool: True if there are zero aliens left, false otherwise 
        """
        return not self.fleet