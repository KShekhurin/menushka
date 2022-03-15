import pygame

resources = {
    "pointer_hand_pic": [None, "pics/рука.png"],

    "menu_button_pic": [None, "pics/кнопка.png"],
    "menu_selector_top_pic": [None, "pics/свиток начало.png"],
    "menu_selector_middle_pic": [None, "pics/свиток середина.jpg"],
    "menu_selector_bottom_pic": [None, "pics/свиток конец.png"],
    "menu_slider_line_pic": [None, "pics/прутик.png"],
    "menu_slider_circle_pic": [None, "pics/мандарин.png"],
    "menu_background_chi_pic": [None, "pics/mao_bg.png"],

    "menu_button_click_snd": [None, "snd/клик.mp3"],
    "menu_button_hover_snd": [None, "snd/струна.wav"],

    "helper_default_pic": [None, "pics/якубович.jpg"],
    "helper_blink_pic": [None, "pics/якубович моргает.jpg"],
    "helper_speak_pic": [None, "pics/автомобиль.jpg"],
    "helper_speak_blink_pic": [None, "pics/автомобиль моргает.jpg"],
    "helper_cloud_pic": [None, "pics/облако.png"],

    "helper_angry_snd": [None, "snd/сварог.wav"],

    "player_default_pic": [None, "pics/гг.png"],

    "scene_field_background_pic": [None, "pics/1 сцена.jpg"],

    "item_plate_pic": [None, "pics/тарелка.png"]
}

def get_res(res_name):
    if not isinstance(res_name, str): return
    if not (res_name in resources.keys()): raise KeyError("[Utils/Assets.py]: Нет такого ресурса: " + str(res_name) + ".")

    if resources[res_name][0] == None:
        if (resources[res_name][1].find(".jpg") != -1 or
            resources[res_name][1].find(".png") != -1):
            resources[res_name][0] = pygame.image.load(resources[res_name][1])
        elif (resources[res_name][1].find(".wav") != -1 or
              resources[res_name][1].find(".mp3") != -1):
           resources[res_name][0] = pygame.mixer.Sound(resources[res_name][1]) 
        else: raise TypeError("[Utils/Assets.py]: Неподдерживаемый формат файла.")
    
    return resources[res_name][0]