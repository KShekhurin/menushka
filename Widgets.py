import pygame


class ButtonDesignParams:
    def __init__(self):
        self.background_color_default = (0, 0, 0)
        self.foreground_color_default = (255, 255, 255)

        self.background_color_selected = (255, 255, 255)
        self.foreground_color_selected = (0, 0, 0)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), size=(10, 10), 
            text="", design: ButtonDesignParams=ButtonDesignParams(), onClick=None, *groups):
        super().__init__(*groups)
        self.x, self.y = pos
        self.h, self.w = size
        self.text = text

        self.onClick = onClick
        self.focused = False

        self.font = pygame.font.Font(None, 36)

        self.design = design
        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def draw(self):
        background = (self.design.background_color_default 
            if not self.focused else self.design.background_color_selected)
        foreground = (self.design.foreground_color_default 
            if not self.focused else self.design.foreground_color_selected)

        self.image.fill(background)
        rendered_text = self.font.render(self.text, True, foreground)

        text_width = rendered_text.get_width()
        text_heigh = rendered_text.get_height()

        self.image.blit(rendered_text, (
                (self.h - text_width) // 2,
                (self.w - text_heigh) // 2
            )
        )
    
    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.focused and self.onClick is not None:
                    self.onClick()

        self.draw()


class Slider(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), size=(10, 10), level=0, *groups):
        super().__init__(*groups)
        self.x, self.y = pos
        self.h, self.w = size
        self.level = level

        self.focused = False
        self.selected = True

        self.font = pygame.font.Font(None, 36)

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.fill((0, 0, 0))

        pygame.draw.line(
            self.image, (255, 255, 255), 
            (self.w // 2, self.w // 2), 
            (self.h - self.w // 2, self.w // 2),
            2
        )

        pygame.draw.circle(
            self.image, (255, 255, 255),
            (self.w // 2  + (self.h - self.w) * self.level, self.w // 2),
            self.w // 5
        )
    
    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False
            self.selected = False

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.focused:
                    self.selected = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = False

        if self.selected:
            relative_x_pos = mouse_pos[0] - self.x

            if relative_x_pos <= self.w // 2:
                self.level = 0
            elif relative_x_pos >= self.h - self.w // 2:
                self.level = 1
            else:
                self.level = (mouse_pos[0] - self.w // 2) / (self.h - self.w)

        self.draw()