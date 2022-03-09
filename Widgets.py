import pygame

default_pic = 'дед2.png'


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

        self.background_pic_surf = pygame.image.load(default_pic)

    def draw(self):
        background = (self.design.background_color_default 
            if not self.focused else self.design.background_color_selected)

        foreground = (self.design.foreground_color_default 
            if not self.focused else self.design.foreground_color_selected)

        self.image.fill(background)
        rendered_text = self.font.render(self.text, True, foreground)

        text_width = rendered_text.get_width()
        text_heigh = rendered_text.get_height()

        if self.focused:
            self.image.blit(self.background_pic_surf, (0, 0))
            #print(self.x, self.y)

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



class Label(pygame.sprite.Sprite):
    def __init__(self, pos, text, *groups) -> None:
        super().__init__(*groups)

        self.text = text

        self.font = pygame.font.Font(None, 36)

        self.rect = pygame.rect.Rect(pos, (0, 0))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
    
    def draw(self):
        rendered_text = self.font.render(self.text, True, (255, 255, 255))

        self.rect = pygame.rect.Rect(
            (self.rect.x, self.rect.y), 
            (rendered_text.get_width(), rendered_text.get_height())
        )

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.blit(rendered_text, (0, 0))
    
    def update(self, *events):
        self.draw()


class Slider(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), rel_pos=(0, 0), size=(10, 10), level=0, on_value_changed=None, *groups):
        super().__init__(*groups)
        self.x, self.y = pos
        self.rel_x, self.rel_y = rel_pos
        self.h, self.w = size
        self.level = level

        self.focused = False
        self.selected = False
        self.on_value_changed = on_value_changed

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
        #Омега лютый костыль, я испытываю праведный стыд каждый раз, когда вижу это.
        mouse_pos = (mouse_pos[0] - self.rel_x, mouse_pos[1] - self.rel_y)

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False

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
            
            if self.on_value_changed is not None:
                self.on_value_changed(self.level)

        self.draw()


class SliderWithValue(pygame.sprite.Sprite):
    def __init__(self, pos, slider_size, level, *groups) -> None:
        super().__init__(*groups)

        self.level = level

        self.inner_group = pygame.sprite.Group()
        self.slider = Slider((0, 0), pos, slider_size, level, self.level_changed, self.inner_group)
        self.label = Label((self.slider.rect.width + 10, 0), self.get_percent(), self.inner_group)

        self.rect = pygame.rect.Rect(pos, (self.slider.rect.width + self.label.rect.width + 10, self.slider.rect.height))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
    
    def level_changed(self, new_level):
        self.level = new_level
        self.label.text = self.get_percent()

    def get_percent(self):
        return str(f"{round(self.level * 100)}%")
    
    def draw(self):
        self.rect = pygame.rect.Rect(
            (self.rect.x, self.rect.y),
            (self.slider.rect.width + self.label.rect.width + 10, self.slider.rect.height)
        )
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.label.rect.y = (self.rect.height - self.label.rect.height) // 2

        self.inner_group.draw(self.image)
    
    def update(self, *events):
        self.inner_group.update(*events)
        
        self.draw()