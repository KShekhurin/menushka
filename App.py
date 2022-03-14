import pygame
from Frames.Frames import Frame

class App:
    def __init__(self, loaded_frame: Frame, start_size=(200, 200)):
        self.start_size = start_size
        self.loaded_frame = loaded_frame

    def start(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        pygame.mixer.music.load('music/славяне.mp3')
        pygame.mixer.music.play(100)
        
        self.screen = pygame.display.set_mode(self.start_size)
        self.run = True

        self.loaded_frame.post_init(self)

        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    if hasattr(self.loaded_frame, "helper"):
                        self.loaded_frame.helper.quit_threads()
                    self.quit()

            #self.screen.fill((0, 0, 255))
            self.loaded_frame.update(events)
            self.loaded_frame.draw(self.screen)

            pygame.display.flip()

    def quit(self):
        self.run = False
    
    def reload_frame(self, new_frame: Frame):
        self.loaded_frame = new_frame
        self.loaded_frame.post_init(self)

    def redraw_frame(self):
        self.loaded_frame.draw(self.screen)