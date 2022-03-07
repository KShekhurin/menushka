import sys
import pygame
from Widgets import Button, ButtonDesignParams, Label, Slider, SliderWithValue


class Frame:
    def __init__(self):
        self.drawable = []
        self.updatable = []

    def post_init(self, app):
        self.app = app

    def append_widget(self, widget):
        self.drawable.append(widget)
        self.updatable.append(widget)

    def append_many_widgets(self, widgets):
        for widget in widgets:
            self.append_widget(widget)

    def update(self, events):
        for updatable in self.updatable:
            updatable.update(events)

    def draw(self, screen):
        for drawable in self.drawable:
            drawable.draw(screen)


class MenuFrame(Frame):
    def __init__(self):
        super().__init__()
    
    def goto_settings(self):
        self.app.reload_frame(SettingsFrame())

    def exit(self):
        sys.exit() # Да, это плохо. Я протяну колбеки, но потом.

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        Button((275, 10 + 300), (250, 70), "Начать игру", ButtonDesignParams(), None, self.buttons_group)
        Button((275, 90 + 300), (250, 70), "Настройки", ButtonDesignParams(), self.goto_settings, self.buttons_group)
        Button((275, 170 + 300), (250, 70), "Выход", ButtonDesignParams(), self.exit, self.buttons_group)

        Label((70, 100), "Съешь ещё больше этих сладких французских булок.", self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))

class SettingsFrame(Frame):
    def __init__(self):
        super().__init__()
    
    def goto_menu(self):
        self.app.reload_frame(MenuFrame())

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        Label((250, 20), "Громкость:", self.buttons_group)
        SliderWithValue((250, 20 + 50), (255, 70), 0, self.buttons_group)

        Button((250, 20 + 150), (300, 70), "Сохранить изменения", ButtonDesignParams(), None, self.buttons_group)
        Button((575, 525), (200, 50), "Вернуться", ButtonDesignParams(), self.goto_menu, self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))