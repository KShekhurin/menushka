import pygame
from threading import Timer

class Helper(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)

        self.pic_default = pygame.image.load("pics/якубович.jpg")
        self.pic_blink = pygame.image.load("pics/якубович моргает.jpg")

        self.blink_timer = pygame.time.get_ticks()

        self.x, self.y = pos
        self.w, self.h = size
        self.focused = False
        self.pic_default = pygame.transform.scale(self.pic_default, (self.w, self.h))
        self.pic_blink = pygame.transform.scale(self.pic_blink, (self.w, self.h))

        self.pic_current = self.pic_default

        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def blink(self):
        self.pic_current = self.pic_blink
        Timer(0.25, self.default).start()

    def default(self):
        self.pic_current = self.pic_default

    def draw(self):
        self.image.blit(self.pic_current, (0, 0))

    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False

        now = pygame.time.get_ticks()
        if now - self.blink_timer >= 4000:
            self.blink_timer = now
            self.blink()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.focused:
                self.blink()
                self.blink_timer = now

        self.draw()