
import sys
from os.path import exists as file_exists
from configparser import ConfigParser
from math import sqrt

from pygame import Color, Rect
from pygame.display import Info as DisplayInfo


CLI_CONF_DEFAULTS = False


def _read_setting(section, key, type_):
    return type_(_settings[section].get(key, _default_settings[section].get(key)))


def _read_range(section, key, default, type_, polarity=1):
    value = _settings[section].get(key, default).replace(' ', '')
    value = list(map(lambda x: polarity * type_(x), value.split(',')))
    value.sort()
    return tuple(value)

for arg in sys.argv[1:]:
    if arg.startswith('-'):
        for key in arg:
            if key == 'd':
                CLI_CONF_DEFAULTS = True


_settings = ConfigParser()
if not CLI_CONF_DEFAULTS and not _settings.read('./settings.ini', 'utf-8'):
    print("Файл с пользовательскими настройками(settings.ini) не обнаружен, ищем настройки по умолчанию.")

_default_settings = ConfigParser()
if not _default_settings.read('./utils/default_settings.ini', 'utf-8'):
    print("Не найден файл с настройками по умолчанию(utils/default_settings.ini), до свидания.")
    raise SystemExit

if CLI_CONF_DEFAULTS:
    _settings = _default_settings
else:
    for section in _default_settings:
        if section not in _settings:
            _settings[section] = {}


# Экран
UNIT_SCALE = _read_setting('game', 'unit_scale', float)
ENEMY_STANDBY_TIMEOUT = 5000 if _read_setting('game', 'enemy_stdby', int) == 1 else 0
FPS = 60  # Макс. кол-во кадров в секунду
#-------------------------------------------------------------------------------

# Служебное, тут лучше ничего не менять.
_di = DisplayInfo()
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (_di.current_w, _di.current_h)
UNIT_SCALE = sqrt(UNIT_SCALE)
scaled = lambda val: val * UNIT_SCALE  # масштабирует значение
rscaled = lambda val: round(scaled(val))  # матабирует и округляет значение
size_rscaled = lambda size: tuple(map(rscaled, size))  # масштабирует и округляет последовательность
WALL_WIDTH = rscaled(50)
WALL_HEIGHT = rscaled(50)
WALL_SIZE = (WALL_WIDTH, WALL_HEIGHT)
TOTAL_LEVEL_SIZE = (WALL_WIDTH * 50, WALL_HEIGHT * 50)
CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
WORLD_RECT = Rect((0, 0), TOTAL_LEVEL_SIZE)
#-------------------------------------------------------------------------------

# Меню
MENU_BG_COLOR = Color('#333377')  # Цвет фона
MENU_BTN_SIZE = (MENU_BTN_WIDTH, MENU_BTN_HEIGHT) = (500, 160)  # Размер кнопок
MENU_BTN_FONT_SIZE = 60  # Размер шрифта кнопок
#-------------------------------------------------------------------------------

# Кнопки
BTN_TXT_USUAL_COLOR = Color('#FFFFFF')   # Цвет обычного текста для кнопок
BTN_TXT_SELECTED_COLOR = Color('#FF8888')   # Цвет текста кнопки, когда она под курсором
BTN_TXT_INACTIVE_COLOR = Color('#AAAAAA')   # Цвет текста кнопки, когда она не активна
BTN_BG_COLOR = Color('#555577')   # Цвет фона кнопки
#-------------------------------------------------------------------------------

# Текстовые метки
LBL_TXT_DEFAULT_COLOR = Color('#FFFFFF')   # Цвет обычного текста меток
#-------------------------------------------------------------------------------

# Игрок
PLAYER_SPEED = scaled(_read_setting('player', 'speed', float))
PLAYER_HP_MAX = _read_setting('player', 'hp', int)
PLAYER_PLASMA_SPEED = scaled(_read_setting('player', 'plasma_speed', float))
PLAYER_PLASMA_OFFSET = _read_range('player', 'plasma_damage', '15, 25', int, -1)
#-------------------------------------------------------------------------------

# Привидение
ENEMY_SPEED = scaled(_read_setting('ghost', 'speed', float))
ENEMY_FRAME_SIZE = size_rscaled((94, 94))   # Размер рамки для столкновений
ENEMY_SHOOT_TIMEOUT = _read_setting('ghost', 'shoot_timeout', int)
ENEMY_VEER_TIMEOUT = _read_range('ghost', 'veer_timeout', '1700, 4300', int)
ENEMY_MAX_SHOOT_DISTANCE = rscaled(_read_setting('ghost', 'max_shoot_distance', int))
ENEMY_HP_MAX = _read_setting('ghost', 'hp', int)
ENEMY_HP_SHOWING_TIMEOUT = 4000   # Длительность отображения здоровья
ENEMY_PLASMA_SPEED = scaled(_read_setting('ghost', 'plasma_speed', float))
ENEMY_PLASMA_OFFSET = _read_range('ghost', 'plasma_damage', '5, 15', int, -1)
#-------------------------------------------------------------------------------

# Привидение-босс
BOSS_ENEMY_SPEED = scaled(_read_setting('bossghost', 'speed', float))
BOSS_ENEMY_FRAME_SIZE = size_rscaled((100, 100))   # Размер рамки для столкновений
BOSS_ENEMY_SHOOT_TIMEOUT = _read_setting('bossghost', 'shoot_timeout', int)
BOSS_ENEMY_VEER_TIMEOUT = _read_range('bossghost', 'veer_timeout', '2000, 4500', int)
BOSS_ENEMY_HP_MAX = _read_setting('bossghost', 'hp', int)
BOSS_ENEMY_SPAWN_DELAY = _read_setting('bossghost', 'spawn', int)
BOSS_ENEMY_PLASMA_SPEED = scaled(_read_setting('bossghost', 'plasma_speed', float))
BOSS_ENEMY_PLASMA_OFFSET = _read_range('bossghost', 'plasma_damage', '10, 20', int, -1)
#-------------------------------------------------------------------------------

# Капкан
TRAP_OFFSET = -_read_setting('trap', 'damage', int)
TRAP_ANIM_TIMEOUT = 333   # Задержка анимации
#-------------------------------------------------------------------------------

# Телепорт
TELEPORT_ANIM_TIMEOUT = 200   # Задержка анимации
#-------------------------------------------------------------------------------

# Датчик ПК-активности
PKL_MAX_DISTANCE = rscaled(1700)   # Макс. расстояние обнаружения
PKL_UPDATE_TIMEOUT = 500   # Задержка между обновлениями значения
#-------------------------------------------------------------------------------

# Сгустки позитива
HEALTHPOINT_OFFSET_RANGE = _read_range('healthpoint', 'heal_amount', '17, 25', int)
HEALTHPOINT_NUMBER = _read_setting('healthpoint', 'number', int)
#-------------------------------------------------------------------------------

# Мебель
FURNITURE_HP = 100   # Здоровье
#-------------------------------------------------------------------------------
