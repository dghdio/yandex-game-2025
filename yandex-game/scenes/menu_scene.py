
from pygame import event, mouse
from pygame.sprite import Group
from pygame.locals import *

from scenes.scene import Scene
from utils.interface import Button, Label
from utils.config import *


class MenuScene(Scene):
    """Меню игры."""

    NUM_OF_BTNS = 3

    def __init__(self, screen):
        super().__init__(screen, MENU_BG_COLOR)
        self.frame_btn = Rect(0, 0, MENU_BTN_WIDTH, MENU_BTN_HEIGHT * MenuScene.NUM_OF_BTNS)
        self.frame_btn.centerx = self.screen_rect.centerx
        self.frame_btn.centery = self.screen_rect.centery + 50

        self.btn_play     = Button("Новая игра", 'newgame',
                                   rectsize=MENU_BTN_SIZE, fontsize=MENU_BTN_FONT_SIZE,
                                   topleft=Button.get_btn_pos(self.frame_btn, 0, MENU_BTN_HEIGHT))
        self.btn_continue = Button("Продолжить", 'continue',
                                   rectsize=MENU_BTN_SIZE, fontsize=MENU_BTN_FONT_SIZE,
                                   topleft=Button.get_btn_pos(self.frame_btn, 1, MENU_BTN_HEIGHT), active=False)
        self.btn_quit     = Button("Выход", 'exit',
                                   rectsize=MENU_BTN_SIZE, fontsize=MENU_BTN_FONT_SIZE,
                                   topleft=Button.get_btn_pos(self.frame_btn, 2, MENU_BTN_HEIGHT))
        self.buttons = Group(self.btn_play, self.btn_continue, self.btn_quit)

        self.lbl_title = Label("Yandex game", fontsize=70,
                               centerx=self.screen_rect.centerx,
                               centery=130)
        self.lbl_v = Label("v1.0", fontsize=24,
                           bottomright=self.screen_rect.bottomright)
        self.lbl_auth = Label("by Andrew Volkov and Ilya Oktaba", fontsize=24,
                              bottomleft=self.screen_rect.bottomleft)
        self.labels = Group(self.lbl_title, self.lbl_v, self.lbl_auth)

    def handle_buttons(self, position):
        for btn in self.buttons:
            if btn.check_pressed(position):
                self.return_code = btn.id
                if btn.id == 'newgame':
                    self.btn_continue.active = True

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                self.return_code = 'exit'
            elif e.type == MOUSEBUTTONDOWN:
                self.handle_buttons(e.pos)

    def update_objects(self):
        self.buttons.update(mouse.get_pos())

    def draw_objects(self):
        self.screen.blit(self.space, (0, 0))
        self.labels.draw(self.screen)
        for btn in self.buttons:
            btn.draw(self.screen)

    def restart(self):
        self.btn_continue.active = False
