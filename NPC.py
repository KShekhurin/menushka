import pygame
from Pointer import PointerState

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, player_pos, size, default_pic, tip, on_hover, on_lose_hover, on_click, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.player_pos = player_pos
        self.w, self.h = size

        self.default_pic = pygame.transform.scale(default_pic, size)
        self.tip = tip

        self.on_hover = on_hover
        self.on_lose_hover = on_lose_hover
        self.on_click = on_click

        self.focused = False
        self.selected = False

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.default_pic, (0, 0))

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and not self.focused:
            self.focused = True
            self.on_hover(self.tip, PointerState.SPEAK)
        elif not self.rect.collidepoint(mouse_pos) and self.focused:
            self.focused = False
            self.on_lose_hover()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.focused and not self.selected:
                    self.selected = True
                    self.on_click(self.player_pos, "zhirik_0")

            if event.type == pygame.MOUSEBUTTONUP and self.selected:
                self.selected = False

        self.draw()