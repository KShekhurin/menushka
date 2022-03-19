from Frames.Frames import Frame
import pygame
from Widgets import *

class DialogueFrameData:
    def __init__(self, background_pic, character_pic, player_pic, character_name):
        self.background_pic = background_pic
        self.character_pic = character_pic
        self.player_pic = player_pic
        self.character_name = character_name

class DialogueFrame(Frame):
    def __init__(self, dialogue_data):
        super().__init__()
        
        self.data = dialogue_data

        self.player_turn = False

        self.background_pic = pygame.transform.scale(self.data.background_pic, (700, 300))

    def post_init(self, app):
        super().post_init(app)

        self.gui_group = pygame.sprite.Group()

        if not self.player_turn:
            self.speaker_pic = Picture((75, 125), (300, 250), self.data.character_pic, self.gui_group)
        else:
            self.speaker_pic = Picture((125, 125), (300, 250), self.data.player_pic, self.gui_group)

        self.append_widget(self.gui_group)

    def draw(self, screen):
        super().draw(screen)

        screen.fill((0, 0, 0))
        screen.blit(self.background_pic, (50, 75))

        self.gui_group.draw(screen)

    def update(self, *events):
        super().update(*events)

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.change_turn()
                    print(self.player_turn)

        self.gui_group.update(*events)

    def change_turn(self):
        self.player_turn = not self.player_turn

        if not self.player_turn:
            self.speaker_pic.kill()
            self.speaker_pic = Picture((100, 125), (300, 250), self.data.character_pic, self.gui_group)
        else:
            self.speaker_pic.kill()
            self.speaker_pic = Picture((300, 125), (300, 250), self.data.player_pic, self.gui_group)