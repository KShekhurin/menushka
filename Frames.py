import sys
import pygame
from Widgets import (Button, ButtonDesignParams, Label, Slider,
                    SliderWithValue, Selector, SelectorDesignParams)
from Helper import Helper
import Config
import Settings

pygame.init()

default_pic = pygame.image.load('pics/сварог.png')
spec_pic1 = pygame.image.load('pics/сварогсхризм.png')
spec_pic2 = pygame.image.load('pics/сварогврн.png')
default_snd = pygame.mixer.Sound('music/сварог.wav')

class Frame:
    def __init__(self):
        self.drawable = []
        self.updatable = []
        self.background = (255, 0, 0) if (Config.current_local == Config.local_chi) else (0, 0, 255)

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
        screen.fill(self.background)
        for drawable in self.drawable:
            drawable.draw(screen)


class MenuFrame(Frame):
    def __init__(self):
        super().__init__()
    
    def goto_settings(self):
        self.app.reload_frame(SettingsFrame())

    def exit(self):
        sys.exit() # Да, это плохо. Я протяну колбеки, но потом.

    def change_localization(self, options):
        lang = options[0]
        if (lang == "русский"):
            Config.current_local = Config.local_rus
            self.background = (0, 0, 255)
        elif (lang == "китайский"):
            Config.current_local = Config.local_chi
            self.background = (255, 0, 0)
        elif (lang == "латинский"):
            Config.current_local = Config.local_lat
            self.background = (0, 0, 255)

        Settings.lang_options = options

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        Button((275, 10 + 300), (250, 70), "новая_игра", ButtonDesignParams(default_pic, default_snd), None, self.buttons_group)
        Button((275, 90 + 300), (250, 70), "настройки", ButtonDesignParams(default_pic, default_snd), self.goto_settings, self.buttons_group)
        Button((275, 170 + 300), (250, 70), "выйти", ButtonDesignParams(default_pic, default_snd), self.exit, self.buttons_group)

        Label(("center", 100), "рыба", True, self.buttons_group)

        Selector((0, 0), (200, 50), Settings.lang_options, SelectorDesignParams(spec_pic2, default_snd),self.change_localization, self.buttons_group)

        helper = Helper((0, Config.screen_height - 200), (200, 200), self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))

class SettingsFrame(Frame):
    def __init__(self):
        super().__init__()
        self.volume = Settings.volume
    
    def goto_menu(self):
        self.app.reload_frame(MenuFrame())

    def save_changes(self):
        Settings.volume = self.volume
        pygame.mixer.music.set_volume(self.volume)
        default_snd.set_volume(self.volume)

    def update_volume(self, new_volume):
        self.volume = new_volume

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        Label((250, 20), "громкость", True, self.buttons_group)
        SliderWithValue((250, 20 + 50), (255, 70), self.volume, self.update_volume, self.buttons_group)

        Button((250, 20 + 150), (300, 70), "сохранить_изменения", ButtonDesignParams(spec_pic1, default_snd), self.save_changes, self.buttons_group)
        Button((575, 525), (200, 50), "вернуться", ButtonDesignParams(spec_pic2, default_snd), self.goto_menu, self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))