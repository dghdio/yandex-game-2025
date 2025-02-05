
import sys
from pygame import mixer
from pygame import init as pg_init, display, quit as pg_quit
from pygame.locals import FULLSCREEN

pg_init()

from scenes.main_scene import MainScene
from scenes.menu_scene import MenuScene
from scenes.gamover_scene import GameOverScene
from utils.config import *

mixer.init()
mixer.music.load('resources/[Out of Flux - Topic] Bring the Dessert (7f-ZXyL0kDE).mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)
sound_on = True
def init_game():
    screen = display.set_mode(SCREEN_SIZE, FULLSCREEN)
    display.set_caption("Yandex game")
    return screen


if __name__ == '__main__':
    if sys.platform == 'win32':
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except (OSError, FileNotFoundError):
            pass

    screen = init_game()
    menu = MenuScene(screen)
    game = MainScene(screen)
    end = GameOverScene(screen)

    while True:
        event_code = menu.mainloop()
        if event_code == 'exit':
            pg_quit()
            break
        else:
            if event_code == 'newgame':
                game.restart()
                event_code = game.mainloop()
            elif event_code == 'continue':
                event_code = game.mainloop()
            elif event_code == 'gameover':
                end.set_stats(game.stats)
                end.mainloop()
                menu.restart()
            elif event_code == 'mute' and sound_on == True:
                mixer.music.pause()
                sound_on = False
            elif event_code == 'mute' and sound_on == False:
                mixer.music.unpause()
                sound_on = True