import pygame

from Pointer import PointerState

class Portal(pygame.sprite.Sprite):
    def __init__(self, lu, rd, dest_id, on_hover, on_lose_hover, on_click, *groups):
        super().__init__(*groups)

        self.lu, self.rd = lu, rd
        self.x, self.y = self.lu
        self.w, self.h = self.rd[0]- self.lu[0], self.rd[1] - self.lu[1]
        self.dest_id = dest_id
        self.on_hover = on_hover
        self.on_lose_hover = on_lose_hover
        self.on_click = on_click

        self.rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)

        self.focused = False
        self.selected = False

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.focused:
            self.focused = True
            self.on_hover(self.dest_id, PointerState.GOTO)
        elif not self.rect.collidepoint(mouse_pos) and self.focused:
            self.focused = False
            self.on_lose_hover()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.focused and not self.selected:
                    self.selected = True
                    self.on_click(self.dest_id)

            if event.type == pygame.MOUSEBUTTONUP and self.selected:
                self.selected = False