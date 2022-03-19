import pygame
from Frames.Frames import Frame
from Frames.MenuFrame import MenuFrame
from Pointer import Pointer
from Utils.Assets import get_res
import Utils.Config as Config
import Utils.Settings as Settings
import Utils.Saves as Saves
import os

class App:
    def __init__(self, loaded_frame: Frame, start_size=(200, 200)):
        self.start_size = start_size
        self.loaded_frame = loaded_frame
        self.clock = None

    def start(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()

        Saves.load_settings()

        music = ""
        if Config.current_local == Config.local_rus: music = "music/славяне.mp3"
        if Config.current_local == Config.local_chi: music = "music/китайцы.mp3"
        if Config.current_local == Config.local_lat: music = "music/римские.mp3"
        #pygame.mixer.music.load(music)
        #pygame.mixer.music.play(100)
        pygame.mixer.music.set_volume(Settings.music_volume)
        
        self.screen = pygame.display.set_mode(self.start_size)
        pygame.display.set_caption(Config.window_title)
        self.run = True

        pygame.mouse.set_visible(False)
        self.pointer = Pointer(pygame.mouse.get_pos(), (40, 60))

        self.loaded_frame.post_init(self)

        while self.run:
            dt = self.clock.tick(60)
            Settings.dt = dt

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    if hasattr(self.loaded_frame, "helper"):
                        self.loaded_frame.helper.quit_threads()
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.loaded_frame.is_non_game_frame():
                        self.reload_frame(MenuFrame())

            #self.screen.fill((0, 0, 255))
            self.pointer.update_pos(pygame.mouse.get_pos())

            self.loaded_frame.update(events)
            self.loaded_frame.draw(self.screen)

            self.pointer.draw(self.screen)

            pygame.display.flip()

    def quit(self):
        self.run = False
        # удаление временных файлов
        if os.path.exists("tmp"):
            if os.path.isfile("tmp/screenshot.jpg"): os.remove("tmp/screenshot.jpg")
            os.rmdir("tmp")   
    
    def reload_frame(self, new_frame: Frame):
        self.loaded_frame = new_frame
        self.loaded_frame.post_init(self)

    def redraw_frame(self):
        self.loaded_frame.draw(self.screen)