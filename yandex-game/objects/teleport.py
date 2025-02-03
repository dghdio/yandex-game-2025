
from pygame.sprite import collide_rect, spritecollideany, Sprite
from pygame.transform import rotate

from utils.timers import RegularTimer
from utils.assets import teleport_images, teleport_sound
from utils.config import *


class Teleport(Sprite):
    """Телепорт."""

    images = teleport_images

    def __init__(self, x, y, id, tgt_id):
        super().__init__()
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.id = id
        self.tgt_id = tgt_id
        self.active = True
        self.current_anim_id = 0
        self.anim_timer = RegularTimer(self._change_anim, TELEPORT_ANIM_TIMEOUT)

    def _change_anim(self):
        """Вращение."""
        self.image = rotate(self.image, 90)

    def update(self, scene):
        if self.active and self.tgt_id:
            tgt_teleport = self.get_tp_by_id(scene.teleports, self.tgt_id)
            if collide_rect(self, scene.player):
                teleport_sound.play()
                scene.player.rect.center = tgt_teleport.rect.center
                tgt_teleport.active = False
            enemy = spritecollideany(self, scene.enemies)
            if enemy:
                teleport_sound.play()
                enemy.frame_rect.center = tgt_teleport.rect.center
                tgt_teleport.active = False
        else:
            is_overlayed = False
            if collide_rect(self, scene.player):
                is_overlayed = True
            if spritecollideany(self, scene.enemies, lambda s1, s2: s1.rect.colliderect(s2.frame_rect)):
                is_overlayed = True
            self.active = not is_overlayed
        self.anim_timer.update(scene.delta_time)

    @staticmethod
    def get_tp_by_id(group, teleport_id):
        """Получить телепорт из группы по id."""
        for tp in group:
            if tp.id == teleport_id:
                return tp
