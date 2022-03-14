from sre_constants import SRE_FLAG_ASCII
import pygame
from Utils.Assets import get_res
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size

        self.speed = 2.0
        self.dest_x, self.dest_y = 0, 0
        self.is_moving = False
        self.foot_x, self.foot_y = self.x + self.w//2, self.y + self.h

        self.default_pic = pygame.transform.scale(get_res("player_default_pic"), size)

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.blit(self.default_pic, (0, 0))

    def update(self, *events):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dest_x, self.dest_y = mouse_x, mouse_y
                self.is_moving = True

        if self.is_moving:
            if self.foot_x != self.dest_x or self.foot_y != self.dest_y:
                self.move()
            else:
                self.is_moving = False

        self.draw()

    def move(self):
        x_sign, y_sign = 0, 0
        if self.foot_x != self.dest_x:
            x_sign = ((self.dest_x-self.foot_x)/abs(self.dest_x-self.foot_x))
        if self.foot_y != self.dest_y:
            y_sign = ((self.dest_y-self.foot_y)/abs(self.dest_y-self.foot_y))
        dx, dy = 0, 0
        if self.foot_x != self.dest_x:
            dx = 1 * x_sign
        if self.foot_y != self.dest_y:
            dy = 1 * y_sign
        self.rect.move_ip((dx, dy))
        self.x += dx
        self.y += dy
        self.foot_x, self.foot_y = self.x + self.w//2, self.y + self.h