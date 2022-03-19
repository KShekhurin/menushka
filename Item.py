import pygame
from Pointer import PointerState
import Utils.Config as Config
from Utils.Assets import get_res

class ItemData:
    def __init__(self, pos, player_pos, size, default_pic, tip):
        self.x, self.y = pos
        self.w, self.h = size

        self.default_pic = pygame.transform.scale(get_res(default_pic), (self.w, self.h))
        self.player_pos = player_pos
        
        self.tip = tip

class Item(pygame.sprite.Sprite):
    def __init__(self, item_loc_data, on_focuse, on_lose_focuse, on_left_click, on_right_click, *groups):
        super().__init__(*groups)

        self.id = item_loc_data[0]
        print(*item_loc_data[1:])
        self.data = ItemData(*item_loc_data[1:], *Config.items_data[self.id])

        self.rect = pygame.rect.Rect((self.data.x, self.data.y), (self.data.w, self.data.h))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.on_focuse = on_focuse
        self.on_lose_focuse = on_lose_focuse
        self.on_left_click = on_left_click
        self.on_right_click = on_right_click

        self.focused = False
        self.selected = False

    def draw(self):

        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.data.default_pic, (0, 0))
        if self.focused:
            self.__draw_stroke(2)
        else:
            self.__draw_stroke(1)

    def __draw_stroke(self, stroke_width):
        mask = pygame.mask.from_surface(self.data.default_pic)
        mask_outline = mask.outline()
        pygame.draw.lines(self.image, (0, 0, 0), True, mask_outline, stroke_width)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.focused:
            self.focused = True
            self.on_focuse(self.data.tip, PointerState.PICKUP)
        elif not self.rect.collidepoint(mouse_pos) and self.focused:
            self.focused = False
            self.on_lose_focuse()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.selected and self.focused:
                self.selected = True
                if event.button == 1:
                    self.on_left_click(self, self.data.player_pos)

            if event.type == pygame.MOUSEBUTTONUP and self.selected:
                self.selected = False

        self.draw()

    def delete(self):
        self.kill()