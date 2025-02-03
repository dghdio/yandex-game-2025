

from collections import deque

from pygame.sprite import Sprite, spritecollideany

from objects.plasma import PlayerPlasma
from objects.pools import PoolableObject
from utils.util import handle_collision
from utils.ultimate_animation import UltimateAnimation
from utils.timers import RegularTimer
from utils.assets import trap_images, plasm_anim
from utils.config import *


class Trap(Sprite, PoolableObject):
    """Капкан для привидений."""

    images = trap_images
    pool = deque()

    def __init__(self, center):
        super().__init__()
        self.reset(center)
        self.anim_timer = RegularTimer(self.change_img, TRAP_ANIM_TIMEOUT)

    def change_img(self):
        """Мигание."""
        if self.image == self.images[1]:
            self.image = self.images[0]
        else:
            self.image = self.images[1]

    def update(self, scene):
        self.anim_timer.update(scene.delta_time)
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(TRAP_OFFSET)
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            handle_collision(enemy.frame_rect, self.rect, enemy.x_vel, enemy.y_vel)
            enemy.change_direction(enemy.x_vel)
        plasm = spritecollideany(self, scene.plasmas)
        if plasm is not None and type(plasm) != PlayerPlasma:
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            plasm.delete(scene.plasmas)

    def reset(self, center):
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=center)
