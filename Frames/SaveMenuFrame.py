from Frames.Frames import NonGameFrame
import pygame
from Widgets import *
from Utils.Assets import get_res
import Utils.Settings as Settings
import Frames.GameFrame as GameFrame
import Frames.SettingsFrame as SettingsFrame
import Frames.SavesFrame as SavesFrame
import Frames.LoadGameFrame as LoadGameFrame
from Item import ItemData
from Perspective import *

class SaveMenuFrame(NonGameFrame):
    def __init__(self):
        super().__init__()

    def goto_settings(self):
        self.helper.save_blink_timer()

        if self.helper.is_speaking():
            self.helper.humble()
        self.helper.quit_threads()
        
        self.app.reload_frame(SettingsFrame.SettingsFrame())
        Settings.prev_frame = SaveMenuFrame

    def start_game(self):
        self.helper.save_blink_timer()
        self.helper.quit_threads()

        items_data = (
            ItemData((562, 319), (80, 80), get_res("menu_slider_circle_pic"), (544, 453), "Мандарин - царь фруктов"),
            ItemData((405, 300), (90, 60), get_res("item_plate_pic"), (398, 450), "Тарелка разукрашенная")
        )
        
        scene_data = GameFrame.GameFrameData((0, 0, 0), get_res("scene_field_background_pic"), (500, 600), TrapezoidPerspective(Config.screen_height, 440, 50, 750, 185, 615), items_data)
        #scene_data = GameFrame.GameFrameData((0, 0, 0), get_res("scene_field_background_pic"), (300, 300), None, items_data)
        self.app.reload_frame(GameFrame.GameFrame(Settings.last_scene_id))
        Settings.prev_frame = SaveMenuFrame

    def goto_saves(self):
        self.helper.save_blink_timer()
        self.helper.quit_threads()
        
        self.app.reload_frame(SavesFrame.SavesFrame())
        Settings.prev_frame = SaveMenuFrame

    def goto_load_game(self):
        self.helper.save_blink_timer()
        self.helper.quit_threads()
        
        self.app.reload_frame(LoadGameFrame.LoadGameFrame())
        Settings.prev_frame = SaveMenuFrame

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

        Button(("center", -150 + 300), (250, 70), "продолжить", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.start_game, self.buttons_group)
        Button(("center", -70 + 300), (250, 70), "сохраниться", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_saves, self.buttons_group)
        Button(("center", 10 + 300), (250, 70), "загрузить", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_load_game, self.buttons_group)
        Button(("center", 90 + 300), (250, 70), "настройки", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_settings, self.buttons_group)
        Button(("center", 170 + 300), (250, 70), "выйти", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.exit, self.buttons_group)

        Selector((0, 0), (150, 120), Settings.lang_options, SelectorDesignParams(selector_pic_top, selector_pic_middle, selector_pic_bottom, btn_click_snd),self.change_localization, None, None, self.buttons_group)

        self.append_many_widgets((self.buttons_group,))
