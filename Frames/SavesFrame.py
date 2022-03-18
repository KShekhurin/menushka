from Frames.Frames import NonGameFrame
import pygame
from Widgets import *
import Utils.Settings as Settings
import Utils.Saves as Saves
import shutil
from Utils.Assets import get_screenshot

class SavesFrame(NonGameFrame):
    def __init__(self):
        super().__init__()

        self.active_slot = None

    def goto_menu(self):
        self.helper.save_blink_timer()

        if self.helper.is_speaking():
            self.helper.humble()
        self.helper.quit_threads()

        self.app.reload_frame(Settings.prev_frame())

        Settings.prev_frame = SavesFrame

    def slot_collided(self):
        for slot in self.save_slots:
            slot.set_collided(True)

    def slot_uncollided(self):
        for slot in self.save_slots:
            slot.set_collided(False)

    def set_active_slot(self, slot):
        if self.active_slot is not None:
            self.active_slot.set_active(False)

        self.active_slot = slot
        slot.set_active(True)

    def save_game(self):
        if self.active_slot is not None:
            slot_index = self.save_slots.index(self.active_slot)

            Saves.save_game(slot_index)

            screenshot = pygame.transform.scale(get_res("screenshot"), (self.active_slot.pic_w-16, self.active_slot.pic_h-16))
            self.active_slot.set_screenshot(screenshot)
            screenshot_filename = "screenshots/screenshot_" + str(slot_index) + ".jpg"
            shutil.copy2("tmp/screenshot.jpg", screenshot_filename)
            Settings.saves_screenshots[slot_index] = screenshot_filename
            Saves.save_settings()

            self.active_slot.set_active(False)
            self.active_slot = None

    def post_init(self, app):

        self.buttons_group = pygame.sprite.Group()

        btn_pic = get_res("menu_button_pic")
        selector_pic_top = get_res("menu_selector_top_pic")
        selector_pic_middle = get_res("menu_selector_middle_pic")
        selector_pic_bottom = get_res("menu_selector_bottom_pic")
        btn_hover_snd = get_res("menu_button_hover_snd")
        btn_click_snd = get_res("menu_button_click_snd")

        self.save_slots = []
        for i in range(0, 2):
            for j in range(0, 4):
                screenshot= get_screenshot(Settings.saves_screenshots[j + i * 4]) if Settings.saves_screenshots[j + i * 4] is not None else get_res("saves_void_save_pic")
                self.save_slots.append(SaveSlot((50 + j*175, 140 + i*130), (165, 120), (165, 100), screenshot, get_res("saves_outline_pic"), "пусто", self.set_active_slot, self.buttons_group))

        Button(("center", 420), (300, 70), "сохранить_игру", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd, 22), self.save_game, self.buttons_group)
        Button((575, 525), (200, 50), "вернуться", ButtonDesignParams(self.background, btn_pic, btn_pic, btn_hover_snd, btn_click_snd), self.goto_menu, self.buttons_group)

        Selector((0, 0), (150, 120), Settings.lang_options, SelectorDesignParams(selector_pic_top, selector_pic_middle, selector_pic_bottom, btn_click_snd),self.change_localization, self.slot_collided, self.slot_uncollided, self.buttons_group)

        self.append_widget(self.buttons_group)

        
        super().post_init(app)

    def draw(self, screen):
        super().draw(screen)