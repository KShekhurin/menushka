import pygame
from enum import Enum
from Utils.Assets import get_res

class PointerState(Enum):
    DEFAULT = 1,
    PICKUP = 2

class Pointer():
    def __init__(self, pos, size):
        self.x, self.y = pos
        self.w, self.h = size

        self.state = PointerState.DEFAULT

        self.state_pics = {
            PointerState.DEFAULT: pygame.transform.scale(get_res("cursor_default_pic"), size),
            PointerState.PICKUP: pygame.transform.scale(get_res("cursor_pickup_pic"), size)
        }

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def set_state(self, new_state: PointerState):
        self.state = new_state

    def update_pos(self, new_pos):
        self.x, self.y = new_pos

    def draw(self, screen):
        screen.blit(self.state_pics[self.state], (self.x - 10, self.y - 10))
