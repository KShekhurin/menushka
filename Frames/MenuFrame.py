from Frames.Frames import *
import Frames.SettingsFrame as SettingsFrame
import Frames.GameFrame as GameFrame
import Frames.LoadGameFrame as LoadGameFrame
from Item import ItemData
from Perspective import *

class MenuFrame(NonGameFrame):
    def __init__(self):
        super().__init__()
    
    def goto_settings(self):
        self.helper.save_blink_timer()

        if self.helper.is_speaking():
            self.helper.humble()
        self.helper.quit_threads()
        
        self.app.reload_frame(SettingsFrame.SettingsFrame())
        Settings.prev_frame = MenuFrame

    def goto_load_game(self):
        self.helper.save_blink_timer()

        if self.helper.is_speaking():
            self.helper.humble()
        self.helper.quit_threads()
        
        self.app.reload_frame(LoadGameFrame.LoadGameFrame())
        Settings.prev_frame = MenuFrame

    def start_game(self):
        self.helper.save_blink_timer()
        self.helper.quit_threads()

        self.app.reload_frame(GameFrame.GameFrame("summer"))
        Settings.prev_frame = MenuFrame

    def exit(self):
        self.helper.quit_threads()
        self.app.quit()

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()

        btn_pic = get_res("menu_button_pic")
        selector_pic_top = get_res("menu_selector_top_pic")
        selector_pic_middle = get_res("menu_selector_middle_pic")
        selector_pic_bottom = get_res("menu_selector_bottom_pic")
        btn_hover_snd = get_res("menu_button_hover_snd")
        btn_click_snd = get_res("menu_button_click_snd")

        
        Button(("center", -70 + 300), (250, 70), "новая_игра", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.start_game, self.buttons_group)
        Button(("center", 10 + 300), (250, 70), "загрузить", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_load_game, self.buttons_group)
        Button(("center", 90 + 300), (250, 70), "настройки", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_settings, self.buttons_group)
        Button(("center", 170 + 300), (250, 70), "выйти", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.exit, self.buttons_group)

        Label(("center", 150), "рыба", True, 26, (Config.screen_width, Config.screen_height), (255, 255, 255), (0, 0, 0), 1, self.buttons_group)

        Selector((0, 0), (150, 120), Settings.lang_options, SelectorDesignParams(selector_pic_top, selector_pic_middle, selector_pic_bottom, btn_click_snd),self.change_localization, None, None, self.buttons_group)

        #self.helper = Helper((0, Config.screen_height - 200), (200, 200), self.buttons_group)
        if Settings.menu_first_time:
            self.helper.set_phrases(Config.helper_greeting_phrases)
            self.helper.say()
            self.change_localization(Settings.lang_options)


            pygame.mixer.music.play(100)
            Settings.menu_first_time = False
        self.append_many_widgets((
            self.buttons_group,
        ))

    def update(self, events):
        super().update(events)