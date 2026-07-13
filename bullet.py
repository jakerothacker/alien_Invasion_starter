import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Bullet(Sprite):
    """A class that inherites from the sprite class

    Args:
        Sprite (class): simple base class for visible objects
    """
    def __init__(self, game:'AlienInvasion'):
        super().__init__()
        self.screen = game.screen
        self.setting = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_w,self.settings.bullet_h))

        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """moves the bullet based off of the speed in settings
        """
        self.y -=self.setting.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """draws the bullet on the screen
        """
        self.screen.blit(self.image, self.rect)
