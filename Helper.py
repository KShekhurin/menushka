import pygame
from threading import Timer
import Config
import random

class Helper(pygame.sprite.Sprite):
    def __init__(self, pos, size, background, *groups):
        super().__init__(*groups)

        self.background = background

        self.pic_default = pygame.image.load("pics/якубович.jpg")
        self.pic_blink = pygame.image.load("pics/якубович моргает.jpg")
        self.pic_speak = pygame.image.load("pics/автомобиль.jpg")
        self.pic_speak_blink = pygame.image.load("pics/автомобиль моргает.jpg")
        self.pic_cloud = pygame.image.load("pics/облако.png")

        self.blink_timer = pygame.time.get_ticks()

        self.x, self.y = pos
        self.w, self.h = size
        self.cloud_h = self.w * 123 // 484
        self.focused = False
        self.pic_default = pygame.transform.scale(self.pic_default, (self.w, self.h))
        self.pic_blink = pygame.transform.scale(self.pic_blink, (self.w, self.h))
        self.pic_speak = pygame.transform.scale(self.pic_speak, (self.w, self.h))
        self.pic_speak_blink = pygame.transform.scale(self.pic_speak_blink, (self.w, self.h))
        self.pic_cloud = pygame.transform.scale(self.pic_cloud, (self.w, self.cloud_h))

        self.pic_current = self.pic_default

        self.isSpeaking = False
        self.phrase = ""
        self.font = pygame.font.Font("Cyberbit.ttf", 14)

        self.motiv_phrases = Config.helper_motivational_phrases

        self.rect = pygame.rect.Rect(self.x, self.y - self.cloud_h+20, self.w, self.h + self.cloud_h-20)
        self.image = pygame.Surface((self.w, self.h + self.cloud_h-20), pygame.SRCALPHA, 32)

    def blink(self):
        self.pic_current = self.pic_blink
        Timer(0.25, self.default).start()
        self.blink_timer = pygame.time.get_ticks()

    def speak_blink(self):
        self.pic_current = self.pic_speak_blink
        Timer(0.25, self.speak).start()
        self.blink_timer = pygame.time.get_ticks()

    def say(self, phrase):
        self.pic_current = self.pic_speak
        self.isSpeaking = True
        self.phrase = phrase

        Timer(len(phrase)*0.1, self.stop_saying).start()

    def say_motiv(self):
        if not self.isSpeaking:
            phrase = self.motiv_phrases[random.randint(0, len(self.motiv_phrases)-1)]
            self.say(phrase)

    def stop_saying(self):
        self.pic_current = self.pic_default
        self.isSpeaking = False
        self.phrase = ""

    def speak(self):
        self.pic_current = self.pic_speak

    def default(self):
        self.pic_current = self.pic_default

    def change_background(self, new_background):
        self.background = new_background

    def draw(self):
        self.image.fill(self.background)

        self.image.blit(self.pic_current, (0, self.cloud_h-20))

        if self.isSpeaking:
            self.image.blit(self.pic_cloud, (0, 0))

            rendered_text = self.font.render(Config.current_local[self.phrase], True, (0, 0, 0))
            self.image.blit(rendered_text, (self.w/2 - rendered_text.get_width()/2, self.cloud_h/2 - rendered_text.get_height()/2))

    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False

        now = pygame.time.get_ticks()
        is_time_to_blink = now - self.blink_timer >= Config.helper_blink_freq
        if is_time_to_blink and not self.isSpeaking:
            self.blink()
        elif is_time_to_blink and self.isSpeaking:
            self.speak_blink()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.focused:
                #self.blink()
                #self.say("Нажимай уже на кнопку!")
                pass

        self.draw()

class PhraseCloud(pygame.sprite.Sprite):
    def __init__(self, pos, size, phrase, *groups):
        super().__init__(*groups)