import json
import os
import Utils.Settings as Settings
import Utils.Config as Config

def save_game(save_num: int):
    f = open("saves/" + str(save_num) + ".json", "w")

    progress = {
        "last_scene_id": Settings.last_scene_id,
        "player_pos": Settings.player_pos,
        "items_pickedup": Settings.items_pickedup,
        "inventory_items": Settings.inventory_items
    }
    prog_json = json.dumps(progress)

    f.write(prog_json)
    f.close()

def load_save(save_num: int):
    f = open("saves/" + str(save_num) + ".json", "r")

    prog_json = f.read()
    f.close()
    progress = json.loads(prog_json)

    Settings.last_scene_id = progress["last_scene_id"]
    Settings.player_pos = progress["player_pos"]
    Settings.items_pickedup = progress["items_pickedup"]
    Settings.inventory_items = progress["inventory_items"]

def load_settings():
    if os.path.isfile("saves/settings.json"):
        f = open("saves/settings.json", "r")

        settings_json = f.read()
        f.close()
        settings = json.loads(settings_json)

        current_local = settings["current_local"]
        if current_local == "chi": Config.current_local = Config.local_chi
        elif current_local == "lat": Config.current_local = Config.local_lat
        else: Config.current_local = Config.local_rus
        Settings.music_volume = settings["music_volume"]
        Settings.sound_volume = settings["sound_volume"]
        Settings.lang_options = settings["lang_options"]
        Settings.saves = settings["saves"]

def save_settings():
    f = open("saves/settings.json", "w")

    current_local = None
    if Config.current_local == Config.local_rus:
        current_local = "rus"
    elif Config.current_local == Config.local_chi:
        current_local = "chi"
    elif Config.current_local == Config.local_lat:
        current_local = "lat"

    settings = {
        "current_local": current_local,
        "music_volume": Settings.music_volume,
        "sound_volume": Settings.sound_volume,
        "lang_options": Settings.lang_options,
        "saves": Settings.saves
    }
    settings_json = json.dumps(settings)

    f.write(settings_json)
    f.close()