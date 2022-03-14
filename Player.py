from sre_constants import SRE_FLAG_ASCII
import pygame
from Utils.Assets import get_res
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size

        self.speed = 0.777
        self.is_moving = False
        self.foot_x, self.foot_y = self.x + self.w//2, self.y + self.h

        self.pos = pygame.Vector2(self.foot_x, self.foot_y)
        self.destination = pygame.Vector2(0, 0)

        self.default_pic = pygame.transform.scale(get_res("player_default_pic"), size)

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.blit(self.default_pic, (0, 0))

    def update(self, *events):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.destination = pygame.Vector2(mouse_x, mouse_y)
                self.is_moving = True

        if self.is_moving:
            movement = self.destination - self.pos
            if movement.length() < self.speed:
                self.pos = self.destination
            elif movement.length() != 0:
                movement.normalize_ip()
                movement *= self.speed
                self.pos += movement
            
            if movement.length() != 0:
                self.rect.midbottom = list(int(v) for v in self.pos)
            else:
                self.is_moving = False

        self.draw()