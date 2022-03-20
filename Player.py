from sre_constants import SRE_FLAG_ASCII
import pygame
from Perspective import RectPerspective
from Utils.Assets import get_res
import Utils.Settings as Settings
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, foot_pos, size, perspective, on_pickup, *groups):
        super().__init__(*groups)

        self.foot_x, self.foot_y = foot_pos
        self.perspective = perspective
        self.scale = self.perspective.get_scale_by_cord(foot_pos)
        self.w, self.h = size

        self.speed = 0.09
        self.is_moving = False
        self.x, self.y = self.foot_x - (self.w*self.scale)//2, self.foot_y - (self.h*self.scale)

        self.foot_pos = pygame.Vector2(self.foot_x, self.foot_y)
        self.destination = pygame.Vector2(0, 0)

        self.default_pic = pygame.transform.scale(get_res("player_default_pic"), (self.w, self.h))

        self.rect = pygame.rect.Rect((self.foot_x, self.foot_y), (self.w, self.h))
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)

        self.__scale()


        self.move_callback = None
        self.on_pickup = on_pickup

        self.pickup_snd = get_res("player_pickup_snd")

    def draw(self):
        self.image.blit(self.default_pic, (0, 0))

        pygame.draw.rect(self.image, (0, 255, 0), pygame.rect.Rect(0, 0, self.w*self.scale, self.h*self.scale), 1)

    def update(self, events):
        self.__scale()

        if self.is_moving:
            self.__smoothly_move()

        self.draw()

    def move_to(self, destination: pygame.Vector2, callback=None):
        if round((self.foot_pos - destination).length(), 0) != 0:
            self.destination = destination
            self.is_moving = True
            self.move_callback = callback
        elif callback is not None:
            callback()

    def pickup_item(self):
        self.pickup_snd.play()
        self.on_pickup()

    def get_pos(self):
        return (int(self.foot_x), int(self.foot_y))

    def __smoothly_move(self):
        speed = self.speed * Settings.dt * self.scale

        movement = self.destination - self.foot_pos
        if movement.length() < speed:
            self.foot_pos = self.destination
            self.x += self.destination.x - self.foot_pos.x
            self.y += self.destination.y - self.foot_pos.y
        elif movement.length() != 0:
            movement.normalize_ip()
            movement *= speed
            self.foot_pos += movement
            self.x += movement.x
            self.y += movement.y * self.scale**4
        
        #print(movement.length())
        if round((self.foot_pos - self.destination).length(), 0) != 0:
            self.rect.midbottom = list(int(v) for v in self.foot_pos)
        else:
            self.is_moving = False
            if self.move_callback is not None:
                self.move_callback()
                self.move_callback = None

    def __scale(self):
        self.scale = self.perspective.get_scale_by_cord(self.foot_pos)
        w = self.w * self.scale
        h = self.h * self.scale
        self.rect = pygame.rect.Rect((self.x, self.y), (w, h))
        #print(self.rect.size)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.default_pic = pygame.transform.scale(get_res("player_default_pic"), (w, h))
        self.foot_x, self.foot_y = self.x + w//2, self.y + h

        self.foot_pos = pygame.Vector2(self.foot_x, self.foot_y)