import pygame

class Pointer():
    def __init__(self, pos, size, default_pic):
        self.x, self.y = pos
        self.w, self.h = size
        self.default_pic = default_pic
        self.default_pic = pygame.transform.scale(self.default_pic, (self.w, self.h))

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def update_pos(self, new_pos):
        self.x, self.y = new_pos

    def draw(self, screen):
        screen.blit(self.default_pic, (self.x, self.y))
