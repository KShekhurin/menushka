from VidPlayer import Video
import pygame
import Config


class ButtonDesignParams:
    def __init__(self, background_color_default=(0, 0, 0), pic_default=None, pic_focused=None, sound_hover=None, sound_click=None, font_size=26):
        self.background_color_default = background_color_default
        self.foreground_color_default = (255, 255, 255)

        self.background_color_selected = (255, 255, 255)
        self.foreground_color_selected = (0, 0, 0)

        self.background_pic_default = pic_default
        self.background_pic_focused = pic_focused
        self.sound_hover = sound_hover
        self.sound_click = sound_click

        self.font_size = font_size


class Button(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), size=(10, 10), 
            text="", design: ButtonDesignParams=ButtonDesignParams(), onClick=None, *groups):
        super().__init__(*groups)
        self.x, self.y = pos
        self.w, self.h = size
        self.text = text

        self.x = self.x if not (self.x == "center") else Config.screen_width/2 - self.w/2
        self.y = self.y if not (self.y == "center") else Config.screen_height/2 - self.h/2

        self.onClick = onClick
        self.focused = False
        self.selected = False
        self.focused_snd_played = False

        self.design = design
        self.rect = pygame.rect.Rect((self.x, self.y), size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.font = pygame.font.Font("Cyberbit.ttf", self.design.font_size)

        self.design.background_pic_default = pygame.transform.scale(self.design.background_pic_default, (self.w, self.h))
        self.design.background_pic_focused = pygame.transform.scale(self.design.background_pic_focused, (self.w, self.h))

    def draw(self):
        background = (self.design.background_color_default 
            if not self.focused else self.design.background_color_selected)
        foreground = (self.design.foreground_color_default 
            if not self.focused else self.design.foreground_color_selected)

        if self.design.background_pic_default is None:
            self.image.fill(background)
        else:
            self.image.blit(self.design.background_pic_default, (0, 0))
        rendered_text = self.font.render(Config.current_local[self.text], True, foreground)

        text_width = rendered_text.get_width()
        text_height = rendered_text.get_height()

        if self.focused:
            self.image.blit(self.design.background_pic_focused, (0, 0))

        self.image.blit(rendered_text, (
                (self.w - text_width) // 2,
                (self.h - text_height) // 2
            )
        )
    
    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True

            if not self.focused_snd_played:
                self.design.sound_hover.play()
                self.focused_snd_played = True
        else:
            self.focused = False

            self.focused_snd_played = False    

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.focused and self.onClick is not None:
                    self.onClick()
                    self.selected = True
                    self.design.sound_click.play()

        self.draw()



class Label(pygame.sprite.Sprite):
    def __init__(self, pos, text, isLocal=True, font_size=26, color=(255, 255, 255), container_size=(Config.screen_width, Config.screen_height), *groups) -> None:
        super().__init__(*groups)

        self.text = text

        self.font = pygame.font.Font("Cyberbit.ttf", font_size)
        self.isLocal = isLocal
        self.color = color
        self.container_size = container_size

        self.x, self.y = pos

        self.rect = pygame.rect.Rect((0, 0), (0, 0))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
    
    def draw(self):
        rendered_text = self.font.render(Config.current_local[self.text] if self.isLocal else self.text, True, self.color)

        x = self.x if not (self.x == "center") else self.container_size[0]/2 - rendered_text.get_width()/2
        y = self.y if not (self.y == "center") else self.container_size[1]/2 - rendered_text.get_height()/2

        self.rect = pygame.rect.Rect(
            (x, y), 
            (rendered_text.get_width(), rendered_text.get_height())
        )

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.blit(rendered_text, (0, 0))
    
    def update(self, *events):
        self.draw()


class Slider(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), rel_pos=(0, 0), size=(10, 10), level=0, background=(0,0,0), line_img=None, circle_img=None, on_value_changed=None, *groups):
        super().__init__(*groups)
        self.x, self.y = pos
        self.rel_x, self.rel_y = rel_pos
        self.w, self.h = size
        self.level = level
        self.background = background

        self.focused = False
        self.selected = False
        self.on_value_changed = on_value_changed

        self.font = pygame.font.Font(None, 36)

        self.line_img = line_img
        self.circle_img = circle_img
        self.line_img = pygame.transform.scale(self.line_img, (self.w, self.h))
        self.circle_img = pygame.transform.scale(self.circle_img, (self.h, self.h))

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        #pygame.draw.line(
        #    self.image, (255, 255, 255), 
        #    (self.w // 2, self.w // 2), 
        #    (self.h - self.w // 2, self.w // 2),
        #    2
        #)
        self.image.blit(self.line_img, (0, 0))

        #pygame.draw.circle(
        #    self.image, (255, 255, 255),
        #    (self.h // 2  + (self.w - self.h) * self.level, self.h // 2),
        #    self.h // 3
        #)
        self.image.blit(self.circle_img, ((self.w - self.h) * self.level, 0))
    
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

            if relative_x_pos <= self.h // 2:
                self.level = 0
            elif relative_x_pos >= self.w - self.h // 2:
                self.level = 1
            else:
                self.level = (mouse_pos[0] - self.h // 2) / (self.w - self.h)
            
            if self.on_value_changed is not None:
                self.on_value_changed(self.level)

        self.draw()

    def change_background(self, new_background):
        self.background = new_background


class SliderWithValue(pygame.sprite.Sprite):
    def __init__(self, pos, slider_size, level, background, line_img, circle_img, on_value_changed, *groups) -> None:
        super().__init__(*groups)

        self.level = level

        self.on_value_changed = on_value_changed

        self.inner_group = pygame.sprite.Group()
        self.slider = Slider((0, 0), pos, slider_size, level, background, line_img, circle_img, self.level_changed, self.inner_group)
        self.label = Label((self.slider.rect.width + 10, 0), self.get_percent(), False, 26, (255, 255, 255), (Config.screen_width, Config.screen_height), self.inner_group)

        self.rect = pygame.rect.Rect(pos, (self.slider.rect.width + self.label.rect.width + 10, self.slider.rect.height))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
    
    def level_changed(self, new_level):
        self.level = new_level
        self.label.text = self.get_percent()
        self.on_value_changed(self.level)

    def get_percent(self):
        return str(f"{round(self.level * 100)}%")

    def change_background(self, new_background):
        self.slider.change_background(new_background)
    
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


class SelectorDesignParams:
    def __init__(self, pic_top=None, pic_middle=None, pic_bottom=None, snd_selected=None):
        self.pic_top = pic_top
        self.pic_middle = pic_middle
        self.pic_bottom = pic_bottom
        self.snd_selected = snd_selected


class SelectorOption(pygame.sprite.Sprite):
    def __init__(self, pos, size, text, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size

        self.text = text
        self.font = pygame.font.Font("Cyberbit.ttf", 22)

        self.focused = False

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
    
    def draw(self):
        foreground = (255, 255, 255) if not self.focused else (0, 0, 0)
        background = (0, 0, 0) if not self.focused else (255, 255, 255)
    
        rendered_text = self.font.render(Config.current_local[self.text], True, (0, 0, 0))

        if self.focused:
            self.image.fill((255, 255, 255, 128))
        else:
            self.image.fill((255, 255, 255, 0))
        #self.image.fill(background)
        self.image.blit(rendered_text, (self.w/2 - rendered_text.get_width()/2, self.h/2 - rendered_text.get_height()/2))

    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False

        self.draw()

    def isFocused(self):
        return self.focused

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text


class Selector(pygame.sprite.Sprite):
    def __init__(self, pos=(0,0), size=(40,10), options=(), design: SelectorDesignParams=SelectorDesignParams(),
                 on_selected_change=None, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size

        self.top_part_h = 96*self.w//242
        self.middle_part_w = 204*self.w//244
        self.middle_part_h = 27*self.w//204
        self.bottom_part_h = 28*self.w//244

        self.font = pygame.font.Font("Cyberbit.ttf", 22)

        self.inner_group = pygame.sprite.Group()
        self.options = []
        for i in range(1, len(options)):
            self.options.append(SelectorOption(((self.w-self.middle_part_w)//2, self.middle_part_h * 2 * (i+1.5)), (self.middle_part_w, self.middle_part_h * 2), options[i], self.inner_group))

        self.selected = False
        self.focused = False
        self.currentOption = options[0] if len(options) > 0 else "пусто"
        self.on_selected_change = on_selected_change

        self.design = design
        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.design.pic_top = pygame.transform.scale(self.design.pic_top, (self.w, self.top_part_h))
        self.design.pic_middle = pygame.transform.scale(self.design.pic_middle, (self.middle_part_w, self.middle_part_h))
        self.design.pic_bottom = pygame.transform.scale(self.design.pic_bottom, (self.w, self.bottom_part_h))

    def draw(self):
        if self.selected:
            self.rect = pygame.rect.Rect((self.x, self.y), (self.w, self.top_part_h + self.bottom_part_h + self.middle_part_h * 4 * len(self.options)))
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        else:
            self.rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        #self.image.fill((0, 0, 0))

        #if self.focused or self.selected:
        #    self.image.blit(self.design.background_pic, (0, 0))
        middle_count = 2
        self.image.blit(self.design.pic_top, (0, 0))
        self.image.blit(self.design.pic_middle, ((self.w-self.middle_part_w)//2, self.top_part_h))
        self.image.blit(self.design.pic_middle, ((self.w-self.middle_part_w)//2, self.top_part_h + self.middle_part_h))
        if self.selected:
            for i in range(0, len(self.options)*2):
                self.image.blit(self.design.pic_middle, ((self.w-self.middle_part_w)//2, self.top_part_h + self.middle_part_h * middle_count))
                middle_count += 1
        #print(middle_count)
        self.image.blit(self.design.pic_bottom, (0, self.top_part_h + self.middle_part_h * middle_count))

        rendered_text = self.font.render(Config.current_local[self.currentOption], True, (0, 0, 0))
        self.image.blit(rendered_text, (self.w/2 - rendered_text.get_width()/2 - 10, self.top_part_h + (self.middle_part_h*2-rendered_text.get_height())//2))

        if not self.selected:
            pygame.draw.line(self.image, (0, 0, 0), (self.w - 40, self.h/2 + 14), (self.w - 35, self.h/2 + 25), 2)
            pygame.draw.line(self.image, (0, 0, 0), (self.w - 30, self.h/2 + 14), (self.w - 35, self.h/2 + 25), 2)
        else:
            pygame.draw.line(self.image, (0, 0, 0), (self.w - 40, self.h/2 + 25), (self.w - 35, self.h/2 + 14), 2)
            pygame.draw.line(self.image, (0, 0, 0), (self.w - 30, self.h/2 + 25), (self.w - 35, self.h/2 + 14), 2)

        if self.selected:
            self.inner_group.draw(self.image)

    def update(self, *events):
        self.inner_group.update(*events)

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
                self.selected = False
                for opt in self.options:
                    if opt.isFocused():
                        tmp = self.currentOption
                        self.currentOption = opt.getText()
                        opt.setText(tmp)
                        options = [self.currentOption] + list(map(lambda x: x.getText(), self.options))
                        self.on_selected_change(options)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.focused and not self.selected:
                self.selected = True

        self.draw()


class Intro(pygame.sprite.Sprite):
    def __init__(self, video_pos, on_end=None, *groups):
        super().__init__(*groups)

        self.on_end = on_end

        self.video = Video(video_pos)
        self.rect = self.rect = pygame.rect.Rect((0, 0), self.video.get_size())
        self.image = pygame.Surface(self.video.get_size())
        self.video.play()
    
    def draw(self):
       self.video.draw_to(self.image, (0, 0))

    def update(self, *events):
        if not self.video.is_playing:
            #У нас миллиарды феритовых коллечек!
            self.on_end()
        
        for event in events[0]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.video.stop()
        
        self.draw()

class Input(pygame.sprite.Sprite):
    def __init__(self, pos, size, placeholder, font_size, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size
        self.x = self.x if self.x != "center" else (Config.screen_width-self.w)/2
        self.y = self.y if self.y != "center" else (Config.screen_height-self.h)/2

        self.placeholder = placeholder
        self.font_size = font_size

        self.inner_group = pygame.sprite.Group()
        self.value = Label(("center", "center"), self.placeholder, True, self.font_size, (128, 128, 128), (self.w, self.h), self.inner_group)

        self.hovered = False
        self.focused = False

        self.text = ""

        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

    def draw(self):
        if self.focused:
            self.image.fill((128, 128, 128))
        else:
            self.image.fill((200, 200, 200))
        bg_white = pygame.Surface((self.w - 4, self.h - 4))
        bg_white.fill((255, 255, 255))
        self.image.blit(bg_white, (2, 2))

        self.inner_group.draw(self.image)

    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.hovered:
            self.hovered = True
        elif not self.rect.collidepoint(mouse_pos) and self.hovered:
            self.hovered = False

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.hovered and not self.focused:
                self.focused = True
                self.value.color = (10, 10, 10)
                self.value.text = self.text
                self.value.isLocal = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.hovered and self.focused:
                self.focused = False
                self.value.color = (100, 100, 100)
                self.value.text = self.placeholder if self.text == "" else self.text
                self.value.isLocal = True if self.value.text == self.placeholder else False

            if event.type == pygame.KEYDOWN and self.focused:
                if pygame.K_a <= event.key <= pygame.K_z or event.key == pygame.K_SPACE:
                    self.text += chr(event.key)
                    self.value.text = self.text
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:len(self.text)-1]
                    self.value.text = self.text

        self.draw()
        self.inner_group.update(*events)