import json
import os
import Settings as Settings
import Config as Config

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
        "lang_options": Settings.lang_options
    }
    settings_json = json.dumps(settings)

    f.write(settings_json)
    f.close()