import pygame
from threading import Timer
import Config
import Settings
import random

pygame.mixer.init()

h_pic_default = pygame.image.load("pics/якубович.jpg")
h_pic_blink = pygame.image.load("pics/якубович моргает.jpg")
h_pic_speak = pygame.image.load("pics/автомобиль.jpg")
h_pic_speak_blink = pygame.image.load("pics/автомобиль моргает.jpg")
h_pic_cloud = pygame.image.load("pics/облако.png")
h_click_snd = pygame.mixer.Sound("music/сварог.wav")

class Helper(pygame.sprite.Sprite):
    def __init__(self, pos, size, background, *groups):
        super().__init__(*groups)

        self.background = background

        self.blink_timer = Settings.helper_blink_timer if Settings.helper_blink_timer != 0 else pygame.time.get_ticks()

        self.x, self.y = pos
        self.w, self.h = size
        self.cloud_h = self.w * 123 // 484
        self.focused = False
        self.pic_default = pygame.transform.scale(h_pic_default, (self.w, self.h))
        self.pic_blink = pygame.transform.scale(h_pic_blink, (self.w, self.h))
        self.pic_speak = pygame.transform.scale(h_pic_speak, (self.w, self.h))
        self.pic_speak_blink = pygame.transform.scale(h_pic_speak_blink, (self.w, self.h))
        self.pic_cloud = pygame.transform.scale(h_pic_cloud, (self.w, self.cloud_h))

        self.pic_current = self.pic_default

        self.isSpeaking = False
        self.showingCloud = False
        self.phrase = ""
        self.phrases = ()
        self.font = pygame.font.Font("Cyberbit.ttf", 14)

        self.motiv_phrases = Config.helper_motivational_phrases
        self.motiv_timer = pygame.time.get_ticks()

        self.rect = pygame.rect.Rect(self.x, self.y - self.cloud_h+20, self.w, self.h + self.cloud_h-20)
        self.image = pygame.Surface((self.w, self.h + self.cloud_h-20), pygame.SRCALPHA, 32)

    def blink(self, duration=0.25):
        self.pic_current = self.pic_blink
        self.tb = Timer(duration, self.default)
        self.tb.start()
        self.blink_timer = pygame.time.get_ticks()

    def speak_blink(self):
        self.pic_current = self.pic_speak_blink
        self.tsb = Timer(0.25, self.speak)
        self.tsb.start()
        self.blink_timer = pygame.time.get_ticks()

    def say(self, phrase=""):
        self.pic_current = self.pic_speak
        self.showingCloud = True
        self.isSpeaking = True
        self.motiv_timer = pygame.time.get_ticks()

        if len(self.phrases) == 0:
            self.phrase = phrase
            self.t1 = Timer(len(phrase)*0.1, self.stop_saying)
            self.t1.start()
        else:
            self.phrase = self.phrases[0]
            self.phrases = self.phrases[1:]
            self.t1 = Timer(len(self.phrase)*0.1, self.pause_saying)
            self.t1.start()
            self.t2 = Timer(len(self.phrase)*0.1+0.2, self.say)
            self.t2.start()

    def set_phrases(self, phrases):
        self.phrases = phrases

    def say_motiv(self):
        has_time_come = pygame.time.get_ticks() - self.motiv_timer >= Config.helper_motivational_phrase_freq
        if not self.isSpeaking and has_time_come:
            phrase = self.motiv_phrases[random.randint(0, len(self.motiv_phrases)-1)]
            self.say(phrase)

    def pause_saying(self):
        self.pic_current = self.pic_default
        self.showingCloud = False

    def stop_saying(self):
        self.pic_current = self.pic_default
        self.showingCloud = False
        self.isSpeaking = False
        self.phrase = ""

    def speak(self):
        self.pic_current = self.pic_speak

    def default(self):
        self.pic_current = self.pic_default

    def change_background(self, new_background):
        self.background = new_background

    def save_blink_timer(self):
        Settings.helper_blink_timer = self.blink_timer

    def is_speaking(self):
        return self.isSpeaking

    def humble(self):
        h_click_snd.play()
        r = random.randint(0, 1)
        if r == 0 or self.isSpeaking:
            self.blink(0.75)
        else:
            R = random.randint(0, len(Config.helper_anger_phrases)-1)
            self.say(Config.helper_anger_phrases[R])

    def quit_threads(self):
        if hasattr(self, "t1"):
            self.t1.cancel()
        if hasattr(self, "t2"):
            self.t2.cancel()

    def draw(self):
        self.image.fill(self.background)

        self.image.blit(self.pic_current, (0, self.cloud_h-20))

        if self.showingCloud:
            self.image.blit(self.pic_cloud, (0, 0))

            rendered_text = self.font.render(Config.current_local[self.phrase], True, (0, 0, 0))
            #rendered_text = self.font.render(self.phrase, True, (0, 0, 0))
            self.image.blit(rendered_text, (self.w/2 - rendered_text.get_width()/2, self.cloud_h/2 - rendered_text.get_height()/2-2))

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
                self.humble()
                #self.blink()
                #self.say("Нажимай уже на кнопку!")
                pass

        self.draw()