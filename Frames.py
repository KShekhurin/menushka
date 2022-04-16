import sys
from tkinter.messagebox import NO
from turtle import update
import pygame
from Widgets import (Button, ButtonDesignParams, Intro, Katana, Label, LivesCounter, Slider,
                    SliderWithValue, Selector, SelectorDesignParams, Spavner, ScoreCounter, Player, KingSpawner)
from Helper import Helper, h_click_snd
import Config
import Settings

pygame.init()

btn_pic = pygame.image.load('pics/кнопка.png')
gbg = pygame.image.load('pics/gbg.jpg')
selector_pic_top = pygame.image.load('pics/свиток начало.png')
selector_pic_middle = pygame.image.load('pics/свиток середина.jpg')
selector_pic_bottom = pygame.image.load('pics/свиток конец.png')
slider_line_img = pygame.image.load('pics/прутик.png')
slider_circle_img = pygame.image.load('pics/мандарин.png')
mao_bg = pygame.image.load('pics/mao_bg.png')
futa_bg = pygame.image.load('pics/futa.png')

btn_click_snd = pygame.mixer.Sound('music/клик.mp3')
btn_hover_snd = pygame.mixer.Sound('music/струна.wav')

pygame.mixer.music.stop()
pygame.mixer.music.unload()

pygame.mixer.music.load('music/yapoichina.mp3')
pygame.mixer.music.queue('music/yaoyschina.mp3')

pygame.mixer.music.play(-1)

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


class NonGameFrame(Frame):
    def __init__(self, block_everithing=False):
        super().__init__()

        self.block_everithing = block_everithing

        self.background = (26,197,0)
        self.background_img = futa_bg
        if Config.current_local == Config.local_chi: 
            self.background = (255, 0, 0)
            self.background_img = mao_bg
        elif Config.current_local == Config.local_lat: 
            self.background = (0, 0, 255)

        self.no_action_timer = pygame.time.get_ticks()
    
    def draw(self, screen):
        if self.block_everithing:
            screen.blit(gbg, (0, 0))
        elif self.background_img is not None:
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
            self.background_img = futa_bg

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            pygame.mixer.music.load('music/yapoichina.mp3')
            pygame.mixer.music.queue('music/yaoyschina.mp3')

            pygame.mixer.music.play(-1)
        elif (lang == "китайский"):
            Config.current_local = Config.local_chi
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('music/китайцы.mp3')
            pygame.mixer.music.play(100)

            self.background_img = mao_bg
        elif (lang == "латинский"):
            Config.current_local = Config.local_lat
            self.background = (0, 0, 255)
            self.background_img = futa_bg

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            pygame.mixer.music.load('music/yapoichina.mp3')
            pygame.mixer.music.queue('music/yaoyschina.mp3')

            pygame.mixer.music.play(-1)

        self.helper.change_background(self.background)
        Settings.lang_options = options


class GameFrame(NonGameFrame):
    def __init__(self):
        super().__init__(True)

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()
        self.katana_group = pygame.sprite.Group()

        self.spawner_group = dict()

        s1 = Spavner(self.katana_group, (0, 225), "right", self.buttons_group)
        s2 = Spavner(self.katana_group, (0, 350), "right", self.buttons_group)
        s3 = Spavner(self.katana_group, (0, 475), "right", self.buttons_group)
        s4 = Spavner(self.katana_group, (550, 225), "notright", self.buttons_group)
        s5 = Spavner(self.katana_group, (550, 350), "notright", self.buttons_group)
        s6 = Spavner(self.katana_group, (550, 475), "notright", self.buttons_group)

        self.spawner_group[pygame.K_t] = s1
        self.spawner_group[pygame.K_g] = s2
        self.spawner_group[pygame.K_v] = s3

        self.spawner_group[pygame.K_y] = s4
        self.spawner_group[pygame.K_h] = s5
        self.spawner_group[pygame.K_b] = s6 

        self.p = Player(self.spawner_group, 5, self.buttons_group)

        LivesCounter(self.p, self.buttons_group)
        ScoreCounter(self.p, self.buttons_group)


        KingSpawner(
            [s1, s2, s3, s4, s5, s6], self.katana_group, self.p, self.buttons_group
        )


        self.append_many_widgets((
            self.buttons_group,
            self.katana_group
        ))

    def update(self, events):
        super().update(events)

    def draw(self, screen):
        super().draw(screen)


class IntroFrame(Frame):
    def __init__(self):
        super().__init__()
    
    def goto_menu(self):
        self.app.reload_frame(MenuFrame())

    def post_init(self, app):
        super().post_init(app)

        self.intro_group = pygame.sprite.Group()
        self.intro = Intro("vids/zast.webm", self.goto_menu, self.intro_group)
        #self.label = Label(("center", 550), "Для проспуска нажмите пробел", False, 26, self.intro_group)

        self.append_many_widgets((
            self.intro_group,
        ))



class MenuFrame(NonGameFrame):
    def __init__(self):
        super().__init__()
    
    def goto_settings(self):
        self.helper.save_blink_timer()

        if self.helper.is_speaking():
            self.helper.humble()
        self.helper.quit_threads()
        
        self.app.reload_frame(SettingsFrame())
    
    def goto_game(self):
        self.helper.save_blink_timer()
        self.helper.quit_threads()
        
        self.app.reload_frame(GameFrame())

    def exit(self):
        self.helper.quit_threads()
        self.app.quit()

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        Button(("center", 10 + 300), (250, 70), "новая_игра", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_game, self.buttons_group)
        Button(("center", 90 + 300), (250, 70), "настройки", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_settings, self.buttons_group)
        Button(("center", 170 + 300), (250, 70), "выйти", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.exit, self.buttons_group)

        Label((550, 10), "рыба", True, 56, self.buttons_group, font="Karate.ttf")

        Selector((0, 0), (150, 120), Settings.lang_options, SelectorDesignParams(selector_pic_top, selector_pic_middle, selector_pic_bottom, btn_click_snd),self.change_localization, self.buttons_group)

        self.helper = Helper((0, Config.screen_height - 200), (200, 200), self.background, self.buttons_group)
        if Settings.menu_first_time:
            self.helper.set_phrases(Config.helper_greeting_phrases)
            self.helper.say()

            pygame.mixer.music.play(100)
            Settings.menu_first_time = False

        self.append_many_widgets((
            self.buttons_group,
        ))

    def update(self, events):
        super().update(events)

        is_time_to_motiv = pygame.time.get_ticks() - self.no_action_timer >= Config.helper_motivational_phrase_freq
        if is_time_to_motiv:
            self.helper.say_motiv()
            self.no_action_timer = pygame.time.get_ticks()

class SettingsFrame(NonGameFrame):
    def __init__(self):
        super().__init__()
        self.sound_volume = Settings.sound_volume
        self.music_volume = Settings.music_volume
    
    def goto_menu(self):
        self.helper.save_blink_timer()

        if self.helper.is_speaking():
            self.helper.humble()
        self.helper.quit_threads()

        self.app.reload_frame(MenuFrame())

    def save_changes(self):
        self.no_action_timer = pygame.time.get_ticks()

        Settings.sound_volume = self.sound_volume
        Settings.music_volume = self.music_volume
        pygame.mixer.music.set_volume(self.music_volume)
        btn_click_snd.set_volume(self.sound_volume)
        btn_hover_snd.set_volume(self.sound_volume)
        h_click_snd.set_volume(self.sound_volume)

    def update_sound_volume(self, new_volume):
        self.no_action_timer = pygame.time.get_ticks()

        self.sound_volume = new_volume

    def update_music_volume(self, new_volume):
        self.no_action_timer = pygame.time.get_ticks()

        self.music_volume = new_volume

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        Label(("center", 40), "настройки", True, 36, self.buttons_group)

        Label((175, 120), "громкость_звуков", True, 22, self.buttons_group)
        self.sound_volume_slider = SliderWithValue((380, 110), (255, 70), self.sound_volume, self.background, slider_line_img, slider_circle_img, self.update_sound_volume, self.buttons_group)
        Label((175, 230), "громкость_музыки", True, 22, self.buttons_group)
        self.music_volume_slider = SliderWithValue((380, 220), (255, 70), self.music_volume, self.background, slider_line_img, slider_circle_img, self.update_music_volume, self.buttons_group)

        Button(("center", 340), (300, 70), "сохранить_изменения", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd, 22), self.save_changes, self.buttons_group)
        Button((575, 525), (200, 50), "вернуться", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_menu, self.buttons_group)

        Selector((0, 0), (150, 120), Settings.lang_options, SelectorDesignParams(selector_pic_top, selector_pic_middle, selector_pic_bottom, btn_click_snd),self.change_localization, self.buttons_group)

        self.helper = Helper((0, Config.screen_height - 200), (200, 200), self.background, self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))

    def update(self, events):
        super().update(events)

        is_time_to_motiv = pygame.time.get_ticks() - self.no_action_timer >= Config.helper_motivational_phrase_freq
        if is_time_to_motiv:
            self.helper.say_motiv()
            self.no_action_timer = pygame.time.get_ticks()