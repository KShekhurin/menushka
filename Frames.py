import sys
import pygame
from Widgets import Button, ButtonDesignParams, Label, Slider, SliderWithValue, Selector
import Config

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

        Button((275, 10 + 300), (250, 70), "новая_игра", ButtonDesignParams(), None, self.buttons_group)
        Button((275, 90 + 300), (250, 70), "настройки", ButtonDesignParams(), self.goto_settings, self.buttons_group)
        Button((275, 170 + 300), (250, 70), "выйти", ButtonDesignParams(), self.exit, self.buttons_group)

        Label((70, 100), "рыба", True, self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))

class SettingsFrame(Frame):
    def __init__(self):
        super().__init__()
    
    def goto_menu(self):
        self.app.reload_frame(MenuFrame())

    def change_localization(self, lang):
        print(lang)
        if (lang == "русский"):
            Config.current_local = Config.local_rus
        elif (lang == "китайский"):
            Config.current_local = Config.local_chi
        elif (lang == "латинский"):
            Config.current_local = Config.local_lat

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        Label((250, 20), "громкость", True, self.buttons_group)
        SliderWithValue((250, 20 + 50), (255, 70), 0, self.buttons_group)

        Button((250, 20 + 150), (300, 70), "сохранить_изменения", ButtonDesignParams(), None, self.buttons_group)
        Button((575, 525), (200, 50), "вернуться", ButtonDesignParams(), self.goto_menu, self.buttons_group)

        Selector((0, 0), (200, 50), ("русский", "китайский", "латинский"), self.change_localization, self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))