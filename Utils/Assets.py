import pygame
import Utils.Settings as Settings

resources = {
    "screenshot": [None, "tmp/screenshot.jpg"],

    "cursor_default_pic": [None, "pics/рука.png"],
    "cursor_pickup_pic": [None, "pics/рука хватает.png"],
    "cursor_walk_pic": [None, "pics/сланцы.png"],
    "cursor_goto_pic": [None, "pics/дверь.png"],

    "menu_button_pic": [None, "pics/кнопка.png"],
    "menu_selector_top_pic": [None, "pics/свиток начало.png"],
    "menu_selector_middle_pic": [None, "pics/свиток середина.jpg"],
    "menu_selector_bottom_pic": [None, "pics/свиток конец.png"],
    "menu_slider_line_pic": [None, "pics/прутик.png"],
    "menu_slider_circle_pic": [None, "pics/мандарин.png"],
    "menu_background_chi_pic": [None, "pics/mao_bg.png"],

    "menu_button_click_snd": [None, "snd/клик.mp3"],
    "menu_button_hover_snd": [None, "snd/струна.wav"],

    "saves_void_save_pic": [None, "pics/кирпичи.jpg"],
    "saves_outline_pic": [None, "pics/рамка.png"],

    "helper_default_pic": [None, "pics/якубович.jpg"],
    "helper_blink_pic": [None, "pics/якубович моргает.jpg"],
    "helper_speak_pic": [None, "pics/автомобиль.jpg"],
    "helper_speak_blink_pic": [None, "pics/автомобиль моргает.jpg"],
    "helper_cloud_pic": [None, "pics/облако.png"],

    "helper_angry_snd": [None, "snd/сварог.wav"],

    "player_default_pic": [None, "pics/гг.png"],
    
    "player_pickup_snd": [None, "snd/арфа радость.wav"],

    "inventory_background_pic": [None, "pics/онотоле.png"],

    "scene_open_inventory_btn_def_pic": [None, "pics/мешок закрытый.png"],
    "scene_open_inventory_btn_hover_pic": [None, "pics/мешок открытый.png"],
    "scene_save_btn_def_pic": [None, "pics/береста свернулась.png"],
    "scene_save_btn_hover_pic": [None, "pics/береста.png"],

    "scene_field_background_pic": [None, "pics/2 сцена.jpg"],
    "scene_church_background_pic": [None, "pics/3 сцена.jpg"],

    "item_plate_pic": [None, "pics/тарелка.png"],

    "dialogue_meadow_background_pic": [None, "pics/луг фон.png"],
    "dialogue_zhirik_default_pic": [None, "pics/жирик.png"],
    "dialogue_eminem_default_pic": [None, "pics/эминем.png"],
}

screenshots = {}

def get_res(res_name: str):
    if not isinstance(res_name, str): return
    if not (res_name in resources.keys()): raise KeyError("[Utils/Assets.py]: Нет такого ресурса: " + str(res_name) + ".")

    if resources[res_name][0] == None:
        if (resources[res_name][1].find(".jpg") != -1 or
            resources[res_name][1].find(".png") != -1):
            resources[res_name][0] = pygame.image.load(resources[res_name][1])
        elif (resources[res_name][1].find(".wav") != -1 or
              resources[res_name][1].find(".mp3") != -1):
           resources[res_name][0] = pygame.mixer.Sound(resources[res_name][1]) 
           resources[res_name][0].set_volume(Settings.sound_volume)
        else: raise TypeError("[Utils/Assets.py]: Неподдерживаемый формат файла.")
    
    return resources[res_name][0]

def set_volume(new_volume):
    for key in resources:
        if resources[key][0] is None: continue

        if resources[key][1].find('mp3') != -1 or resources[key][1].find(".wav") != -1:
            resources[key][0].set_volume(new_volume)

def get_screenshot(screenshot_filename: str):
    if not screenshot_filename in screenshots:
        screenshots[screenshot_filename] = pygame.image.load(screenshot_filename)
    
    return screenshots[screenshot_filename]