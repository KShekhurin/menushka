from Frames.Frames import *
import Frames.MenuFrame as MenuFrame

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

        self.app.reload_frame(MenuFrame.MenuFrame())

    def save_changes(self):
        self.no_action_timer = pygame.time.get_ticks()

        Settings.sound_volume = self.sound_volume
        Settings.music_volume = self.music_volume
        pygame.mixer.music.set_volume(self.music_volume)
        get_res("menu_button_hover_snd").set_volume(self.sound_volume)
        get_res("menu_button_click_snd").set_volume(self.sound_volume)
        get_res("helper_angry_snd").set_volume(self.sound_volume)

    def update_sound_volume(self, new_volume):
        self.no_action_timer = pygame.time.get_ticks()

        self.sound_volume = new_volume

    def update_music_volume(self, new_volume):
        self.no_action_timer = pygame.time.get_ticks()

        self.music_volume = new_volume

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        btn_pic = get_res("menu_button_pic")
        selector_pic_top = get_res("menu_selector_top_pic")
        selector_pic_middle = get_res("menu_selector_middle_pic")
        selector_pic_bottom = get_res("menu_selector_bottom_pic")
        slider_line_img = get_res("menu_slider_line_pic")
        slider_circle_img = get_res("menu_slider_circle_pic")
        btn_hover_snd = get_res("menu_button_hover_snd")
        btn_click_snd = get_res("menu_button_click_snd")

        Label(("center", 40), "настройки", True, 36, (255, 255, 255), (0, 0, 0), 1, self.buttons_group)

        Label((175, 120), "громкость_звуков", True, 22, (255, 255, 255), (0, 0, 0), 1, self.buttons_group)
        self.sound_volume_slider = SliderWithValue((380, 110), (255, 70), self.sound_volume, self.background, slider_line_img, slider_circle_img, self.update_sound_volume, self.buttons_group)
        Label((175, 230), "громкость_музыки", True, 22, (255, 255, 255), (0, 0, 0), 1, self.buttons_group)
        self.music_volume_slider = SliderWithValue((380, 220), (255, 70), self.music_volume, self.background, slider_line_img, slider_circle_img, self.update_music_volume, self.buttons_group)

        Button(("center", 340), (300, 70), "сохранить_изменения", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd, 22), self.save_changes, self.buttons_group)
        Button((575, 525), (200, 50), "вернуться", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_menu, self.buttons_group)

        Selector((0, 0), (150, 120), Settings.lang_options, SelectorDesignParams(selector_pic_top, selector_pic_middle, selector_pic_bottom, btn_click_snd),self.change_localization, self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))

    def update(self, events):
        super().update(events)

        is_time_to_motiv = pygame.time.get_ticks() - self.no_action_timer >= Config.helper_motivational_phrase_freq
        if is_time_to_motiv:
            self.helper.say_motiv()
            self.no_action_timer = pygame.time.get_ticks()