from sre_constants import SRE_FLAG_ASCII
import pygame
from Perspective import RectPerspective
from Utils.Assets import get_res
import Utils.Settings as Settings
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, perspective, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size

        self.speed = 0.09
        self.is_moving = False
        self.foot_x, self.foot_y = self.x + self.w//2, self.y + self.h

        self.foot_pos = pygame.Vector2(self.foot_x, self.foot_y)
        self.destination = pygame.Vector2(0, 0)

        self.default_pic = pygame.transform.scale(get_res("player_default_pic"), size)

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

        self.perspective = perspective

    def draw(self):
        self.image.blit(self.default_pic, (0, 0))

    def update(self, events):
        if self.is_moving:
            self.__smoothly_move()

        scale = self.perspective.get_scale_by_cord(self.foot_pos)
        self.rect = pygame.rect.Rect((self.x + (self.w - self.w * scale), self.y + (self.h - self.h * scale)), (self.w * scale, self.h * scale))
        #print(self.rect.size)
        self.image = pygame.Surface((self.w * scale, self.h * scale), pygame.SRCALPHA, 32)
        self.default_pic = pygame.transform.scale(get_res("player_default_pic"), (self.w * scale, self.h * scale))
        

        self.draw()

    def move_to(self, destination: pygame.Vector2):
        if self.foot_pos - destination != 0:
            self.destination = destination
            self.is_moving = True

    def __smoothly_move(self):
        movement = self.destination - self.foot_pos
        if movement.length() < self.speed * Settings.dt:
            self.foot_pos = self.destination
            self.x += self.destination.x - self.foot_pos.x
            self.y += self.destination.y - self.foot_pos.y
        elif movement.length() != 0:
            movement.normalize_ip()
            movement *= self.speed * Settings.dt
            self.foot_pos += movement
            self.x += movement.x
            self.y += movement.y
        
        if movement.length() != 0:
            self.rect.midbottom = list(int(v) for v in self.foot_pos)
        else:
            self.is_moving = False