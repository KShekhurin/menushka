import sys
import pygame
from Widgets import (Button, ButtonDesignParams, Label, Slider,
                    SliderWithValue, Selector, SelectorDesignParams)
from Helper import Helper
import Utils.Config as Config
import Utils.Settings as Settings
from Utils.Assets import get_res

class Frame:
    def __init__(self):
        self.drawable = []
        self.updatable = []

    def post_init(self, app):
        self.app = app
        self.helper_group = pygame.sprite.Group()

        self.helper = Helper((0, Config.screen_height - 200), (200, 200), self.helper_group)
        self.append_widget(self.helper_group)

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

    def is_non_game_frame(self):
        return False


class NonGameFrame(Frame):
    def __init__(self):
        super().__init__()

        self.mao_bg = get_res("menu_background_chi_pic")

        self.background = (26,197,0)
        self.background_img = None
        if Config.current_local == Config.local_chi: 
            self.background = (255, 0, 0)
            self.background_img = self.mao_bg
        elif Config.current_local == Config.local_lat: 
            self.background = (0, 0, 255)

        self.no_action_timer = pygame.time.get_ticks()
    
    def draw(self, screen):
        if self.background_img is not None:
            screen.blit(self.background_img, (0, 0))
        else:
            screen.fill(self.background)
        return super().draw(screen)
    
    def change_localization(self, options):
        self.no_action_timer = pygame.time.get_ticks()

        lang = options[0]
        if (lang == "русский"):
            Config.current_local = Config.local_rus
            self.background = (26,197,0)
            self.background_img = None

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('music/славяне.mp3')
            pygame.mixer.music.play(100)
        elif (lang == "китайский"):
            Config.current_local = Config.local_chi
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('music/китайцы народные.mp3')
            pygame.mixer.music.play(100)

            self.background_img = self.mao_bg
        elif (lang == "латинский"):
            Config.current_local = Config.local_lat
            self.background = (0, 0, 255)
            self.background_img = None

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('music/римские.mp3')
            pygame.mixer.music.play(100)
            
        Settings.lang_options = options

    def update(self, *events):
        super().update(*events)

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.helper.rect.collidepoint(event.pos) and event.button == 1:
                    self.helper.humble()

    def is_non_game_frame(self):
        return True