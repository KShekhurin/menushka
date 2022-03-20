from email.policy import default
from sre_constants import SRE_FLAG_ASCII
from xml.dom.expatbuilder import parseString
from Frames.Frames import Frame
import pygame
from Widgets import *
import Utils.Settings as Settings
from enum import Enum
import Frames.GameFrame as GameFrame

class DialogueFrameData:
    def __init__(self, background_pic, dialogue_id):
        self.background_pic = background_pic
        self.character_id = Config.dialogues_data[dialogue_id][0]
        self.character_pics = Config.dialogue_characters_data[self.character_id][1]
        self.player_pics = Config.dialogue_characters_data["player"][1]
        self.character_name = Config.dialogue_characters_data[self.character_id][2]
        self.character_color = Config.dialogue_characters_data[self.character_id][0]
        self.player_color = Config.dialogue_characters_data["player"][0]
        self.player_name = Config.dialogue_characters_data["player"][2]
        self.actions = Config.dialogues_data[dialogue_id][1]

class DialoguePhrase(pygame.sprite.Sprite):
    def __init__(self, pos, size, text_color, max_length, typing_freq, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size
        self.text = ""
        self.text_color = text_color
        self.max_len = max_length

        self.labels_group = pygame.sprite.Group()
        self.labels = []
        self.labels.append(Label(("center", 0), "", False, 24, (Config.screen_width, Config.screen_height), text_color, (0, 0, 0), 0, self.labels_group))
        self.label_index = 0

        self.text_buffer = ""
        self.text_typing = ""
        self.typing_timer = pygame.time.get_ticks()
        self.is_typing = False
        self.typing_freq = typing_freq
        self.to_wrap = False

        self.rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.labels_group.draw(self.image)

    def update(self, *events):
        self.labels_group.update(*events)
        if self.is_typing:
            now = pygame.time.get_ticks()

        if self.is_typing and now - self.typing_timer >= self.typing_freq:
            self.__show_text_line()
            self.typing_timer = now

        self.draw()

    def say(self, text):
        self.text = text
        self.text_typing = text
        self.is_typing = True

    def complete(self):
        self.is_typing = False
        self.text_buffer = self.text_typing
        for label in self.labels:
            label.kill()
            del label
        del self.labels
        self.labels = []
        self.label_index = 0

        if len(self.text_buffer) >= self.max_len:
            while len(self.text_buffer) >= self.max_len:
                self.labels.append(Label(("center", 22 * self.label_index), "", False, 24, (Config.screen_width, Config.screen_height), self.text_color, (0, 0, 0), 0, self.labels_group))

                self.labels[self.label_index].text = self.text_buffer[:self.max_len]
                self.text_buffer = self.text_buffer[self.max_len:]
                self.to_wrap = True

                buf_len = len(self.text_buffer)
                for i in range(0, buf_len):
                    if self.text_buffer[i] == " ":
                        self.labels[self.label_index].text += self.text_buffer[:i]
                        self.text_buffer = self.text_buffer[i+1:]
                        
                        self.label_index += 1
                        self.to_wrap = False
                        break
            
            if len(self.text_buffer) > 0 and not self.to_wrap:
                self.labels.append(Label(("center", 22 * self.label_index), self.text_buffer, False, 24, (Config.screen_width, Config.screen_height), self.text_color, (0, 0, 0), 0, self.labels_group))
            elif len(self.text_buffer) > 0:
                self.labels[self.label_index].text += self.text_buffer
        else:
            self.labels.append(Label(("center", 22 * self.label_index), self.text_buffer, False, 24, (Config.screen_width, Config.screen_height), self.text_color, (0, 0, 0), 0, self.labels_group))

    def clear(self, new_color):
        self.text = self.text_buffer = self.text_typing = ""
        for label in self.labels:
            label.kill()
            del label
        del self.labels
        self.labels = []
        self.text_color = new_color
        self.labels.append(Label(("center", 0), "", False, 24, (Config.screen_width, Config.screen_height), self.text_color, (0, 0, 0), 0, self.labels_group))
        self.label_index = 0
        self.to_wrap = False

    def __show_text_line(self):
        if len(self.text) > 0:
            self.text_buffer += self.text[0]
            if len(self.text_buffer) > self.max_len:
                self.to_wrap = True

            if self.to_wrap and self.text[0] == " ":
                self.label_index += 1
                self.text_buffer = self.text[0]
                self.labels.append(Label(("center", 22 * self.label_index), "", False, 24, (Config.screen_width, Config.screen_height), self.text_color, (0, 0, 0), 0, self.labels_group))
                self.to_wrap = False

            self.text= self.text[1:]
            self.labels[self.label_index].text = self.text_buffer
        else:
            self.is_typing = False

class DialogueCharacter(pygame.sprite.Sprite):
    def __init__(self, rel_pos, size, bg_pos, bg_size, pic_dict, current_state, active, *groups):
        super().__init__(*groups)

        self.x, self.y = rel_pos
        self.w, self.h = size
        self.pic_dict = pic_dict.copy()
        print(pic_dict)
        for key in self.pic_dict:
            self.pic_dict[key] = pygame.transform.scale(get_res(self.pic_dict[key]), size)
        self.current_state = current_state

        self.bg_x, self.bg_y = bg_pos
        self.bg_w, self.bg_h = bg_size

        self.is_anim = False
        self.target_x, self.target_y = rel_pos
        self.speed = 0.03

        self.active = active

        self.rect = pygame.rect.Rect(bg_pos, bg_size)
        self.image = pygame.Surface(bg_size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.fill((255, 255, 255, 0))

        if self.active:
            self.image.blit(self.pic_dict[self.current_state], (self.x, self.y))

    def update(self, *events):
        if self.is_anim:
            self.__smoothly_move()

        self.draw()

    def set_active(self, a):
        self.active = a

    def anim(self, animation):
        self.is_anim = True

        match animation:
            case "appear_left":
                self.target_x = self.x
                self.x = 0
                return
            case "appear_right":
                self.target_x = self.x
                self.x = self.bg_w - self.w
                return
            case "none":
                return

    def complete_anim(self):
        self.x = self.target_x
        self.y = self.target_y
        self.is_anim = False

    def change_state(self, new_state):
        self.current_state = new_state

    def __smoothly_move(self):
        dx = 1 if self.x < self.target_x else -1
        if self.x == self.target_x: dx = 0
        dy = 1 if self.y < self.target_y else -1
        if self.y == self.target_y: dy = 0

        if abs(self.x - self.target_x) < self.speed * Settings.dt:
            self.x = self.target_x
        else:
            self.x += dx * self.speed * Settings.dt

        if abs(self.y - self.target_y) < self.speed * Settings.dt:
            self.y = self.target_y
        else:
            self.y += dy * self.speed * Settings.dt
        
        if self.y == self.target_y and self.x == self.target_x:
            self.is_anim = False

class DialogueFrame(Frame):
    def __init__(self, dialogue_data):
        super().__init__()
        
        self.data = dialogue_data
        self.act_index = 0

        self.player_turn = self.data.actions[0][0]

        self.background_pic = pygame.transform.scale(self.data.background_pic, (700, 300))

    def post_init(self, app):
        super().post_init(app)

        self.gui_group = pygame.sprite.Group()

        self.character_name_label = Label(("center", 10), self.data.character_name, False, 40, (Config.screen_width, Config.screen_height), (255, 255, 255), (0, 0, 0), 2, self.gui_group)

        text_color = self.data.player_color if self.player_turn else self.data.character_color

        self.character_spr = DialogueCharacter((50, 50), (300, 250), (50, 75), (700, 300), self.data.character_pics, "default", not self.player_turn, self.gui_group)
        self.player_spr = DialogueCharacter((350, 50), (300, 250), (50, 75), (700, 300), self.data.player_pics, "default", self.player_turn, self.gui_group)

        self.phrase = DialoguePhrase((0, 400), (Config.screen_width, 200), text_color, 40, 40, self.gui_group)

        self.act_further()

        self.append_widget(self.gui_group)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.background_pic, (50, 75))

        self.gui_group.draw(screen)
        
        super().draw(screen)

    def update(self, *events):
        super().update(*events)
        now = pygame.time.get_ticks()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.phrase.is_typing or self.character_spr.is_anim or self.player_spr.is_anim:
                        self.phrase.complete()
                        self.character_spr.complete_anim()
                        self.player_spr.complete_anim()
                    elif self.act_index < len(self.data.actions):
                        self.act_further()
                    else:
                        self.app.reload_frame(GameFrame.GameFrame(Settings.last_scene_id))

        self.gui_group.update(*events)

    def act_further(self):
        color = self.data.player_color if self.player_turn else self.data.character_color
        self.phrase.clear(color)

        self.player_spr.set_active(self.player_turn)
        self.character_spr.set_active(not self.player_turn)

        if self.player_turn:
            self.player_spr.anim(self.data.actions[self.act_index][2])
            self.player_spr.change_state(self.data.actions[self.act_index][1])
            self.character_name_label.text = self.data.player_name
        else:
            self.character_spr.anim(self.data.actions[self.act_index][2])
            self.character_spr.change_state(self.data.actions[self.act_index][1])
            self.character_name_label.text = self.data.character_name

        self.phrase.say(self.data.actions[self.act_index][3])

        self.act_index += 1
        if self.act_index < len(self.data.actions):
            self.player_turn = self.data.actions[self.act_index][0]

    def change_turn(self):
        self.player_turn = not self.player_turn
        color = self.data.player_color if self.player_turn else self.data.character_color

        self.character_spr.change_state("wtf")

        if self.player_turn:
            self.player_spr.anim("appear_right")

        self.phrase.clear(color)
        self.phrase.say("self.labels.append(Label((\"center\", 0), \"\", False, 24, (Config.screen_width, Config.screen_height), text_color, (0, 0, 0), 2, self.labels_group))")