

from pygame.image import load
from pygame.mixer import Sound
from pygame.transform import rotate, scale
from pyganim import getImagesFromSpriteSheet

from utils.config import *


def load_texture(filename, size):
    """Загружает текстуру и масштабирует её."""
    texture = load(filename)
    scaled_size = size_rscaled(size)
    texture = scale(texture, scaled_size)
    return texture


def get_atlas_rects(rows, cols, width, height):
    """Получает прямоугольники для getImagesFromSpriteSheet."""
    rects = []
    for i in range(rows):
        for j in range(cols):
            x = j * width
            y = i * height
            rects.append((x, y, width, height))
    return rects


def load_texture_atlas(filename, rows, cols, width, height, size=None):
    """Загружает атлас текстур в виде списка Surface-ов."""
    rects = get_atlas_rects(rows, cols, width, height)
    atlas = getImagesFromSpriteSheet(filename, width, height, rows, cols, rects)
    if size is None:
        size = (width, height)
    for i in range(len(atlas)):
        atlas[i] = scale(atlas[i], size_rscaled(size))
    return atlas


print("Загрузка ресурсов...")

# Текстуры
p_img = load_texture('resources/hunter.png', (64, 64))
player_images = (p_img, rotate(p_img, 90), rotate(p_img, 180), rotate(p_img, 270))
enemy_plasma_image = load_texture('resources/gplasma.png', (16, 16))
boss_enemy_plasma_image = load_texture('resources/bgplasma.png', (25, 25))
player_plasma_image = load_texture('resources/pplasma.png', (22, 22))
heal_image = load_texture('resources/heal.png', (25, 25))

# Атласы текстур
enemy_images = load_texture_atlas('resources/ghost.png', 1, 4, 64, 64)
boss_enemy_images = load_texture_atlas('resources/bossghost.png', 1, 4, 70, 70)
sofa_images = load_texture_atlas('resources/sofa.png', 3, 1, 100, 50)
flower_images = load_texture_atlas('resources/flower.png', 1, 3, 50, 50)
teleport_images = load_texture_atlas('resources/teleport.png', 1, 4, 64, 64)
trap_images = load_texture_atlas('resources/trap.png', 1, 2, 32, 32, (48, 48))
enemy_dying_anim = load_texture_atlas('resources/ghostdie.png', 1, 3, 32, 32)
plasm_anim = load_texture_atlas('resources/explasm.png', 1, 3, 32, 32)

# Звуки
enemy_shoot_sound = Sound('resources/gshoot.wav')
enemy_auch_sound = Sound('resources/gauch.wav')
player_auch_sound = Sound('resources/auch.wav')
player_shoot_sound = Sound('resources/pshoot.wav')
player_walk_sound = Sound('resources/walk.wav')
trap_down_sound = Sound('resources/trapdown.wav')
trap_up_sound = Sound('resources/trapup.wav')
furniture_breaking_sound = Sound('resources/break.wav')
teleport_sound = Sound('resources/teleport.wav')
heal_sound = Sound('resources/heal.wav')


print("Готово.")
