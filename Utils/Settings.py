prev_frame = None

dt = 0

sound_volume = 1.0
music_volume = 0.1
lang_options = ("русский", "китайский", "латинский")

helper_blink_timer = 0

menu_first_time = True
settings_first_time = True

saves = {}

# SCENES STATE
last_scene_id = ""
player_pos = [-1, -1]

items_pickedup = {
    "summer": [False, False]
}

inventory_items = []