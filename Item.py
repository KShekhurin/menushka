import pygame

class ItemData:
    def __init__(self, pos, size, default_pic, stroke_width, tip):
        self.x, self.y = pos
        self.w, self.h = size

        self.default_pic = pygame.transform.scale(default_pic, (self.w - 2 * stroke_width, self.h - 2 * stroke_width))
        self.stroke_width = stroke_width
        
        self.tip = tip

class Item(pygame.sprite.Sprite):
    def __init__(self, item_data, on_focuse, on_lose_focuse, *groups):
        super().__init__(*groups)

        self.data = item_data

        self.rect = pygame.rect.Rect((self.data.x, self.data.y), (self.data.w, self.data.h))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.on_focuse = on_focuse
        self.on_lose_focuse = on_lose_focuse

        self.focused = False

    def draw(self):

        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.data.default_pic, (0, 0))
        if self.focused:
            self.__draw_stroke()

    def __draw_stroke(self):
        mask = pygame.mask.from_surface(self.data.default_pic)
        mask_outline = mask.outline()
        pygame.draw.lines(self.image, (0, 0, 0), True, mask_outline, self.data.stroke_width)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.focused:
            self.focused = True
            self.on_focuse(self.data.tip, True)
        elif not self.rect.collidepoint(mouse_pos) and self.focused:
            self.focused = False
            self.on_lose_focuse()

        self.draw()