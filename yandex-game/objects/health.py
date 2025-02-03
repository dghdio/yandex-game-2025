

from random import randint, choice

from pygame.sprite import Sprite, collide_rect

from utils.assets import heal_image, heal_sound
from utils.config import *


class HealthPoint(Sprite):
    """Заряд позитива."""
    image = heal_image

    def __init__(self, position):
        super().__init__()
        self.rect = self.image.get_rect(topleft=position)

    def update(self, scene):
        if collide_rect(self, scene.player):
            heal_sound.play()
            scene.player.shift_hp(randint(*HEALTHPOINT_OFFSET_RANGE))
            self.rect.topleft = choice(scene.hp_spawn_positions)

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        """Создать множество объектов в случайных местах"""
        for i in range(number):
            pos = choice(positions)
            group.add(cls(pos))
