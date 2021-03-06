import pygame
from Pointer import PointerState
import Utils.Config as Config
from Utils.Assets import get_res

class ButtonDesignParams:
    def __init__(self, background_color_default=(0, 0, 0), pic_default=None, pic_focused=None, sound_hover=None, sound_click=None, font_size=26):
        self.background_color_default = background_color_default
        self.foreground_color_default = (255, 255, 255)

        self.background_color_selected = (255, 255, 255)
        self.foreground_color_selected = (255,228,196)

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
                if self.focused and self.onClick is not None and event.button == 1:
                    self.onClick()
                    self.selected = True
                    self.design.sound_click.play()

        self.draw()

class PictureButton(pygame.sprite.Sprite):
    def __init__(self, pos, size, def_pic, hover_pic, tip, on_click, on_hover, on_lose_hover, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size

        self.def_pic = pygame.transform.scale(get_res(def_pic), size)
        self.hover_pic = pygame.transform.scale(get_res(hover_pic), size)

        self.tip = tip
        self.on_click = on_click
        self.on_hover = on_hover
        self.on_lose_hover = on_lose_hover

        self.focused = False
        self.selected = False

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

    def __draw_stroke(self):
        pic = self.def_pic if not self.focused else self.hover_pic
        mask = pygame.mask.from_surface(pic)
        mask_outline = mask.outline()
        pygame.draw.lines(self.image, (0, 0, 0), True, mask_outline, 2)

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        if not self.focused:
            self.image.blit(self.def_pic, (0, 0))
        else:
            self.image.blit(self.hover_pic, (0, 0))

        self.__draw_stroke()

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and not self.focused:
            self.focused = True
            self.on_hover(self.tip, PointerState.DEFAULT)
        elif not self.rect.collidepoint(mouse_pos) and self.focused:
            self.focused = False
            self.on_lose_hover()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.focused:
                if event.button == 1 and not self.selected:
                    self.selected = True
                    self.on_click()

            if event.type == pygame.MOUSEBUTTONUP and self.selected:
                self.selected = False

        self.draw()

class Label(pygame.sprite.Sprite):
    def __init__(self, pos, text, isLocal=True, font_size=26, rel_size=(Config.screen_width, Config.screen_height), color=(255, 255, 255), outline_color=(0,0,0), outline_w=0, *groups) -> None:
        super().__init__(*groups)

        self.text = text

        self.font = pygame.font.Font("Cyberbit.ttf", font_size)
        self.isLocal = isLocal
        self.color = color
        self.outline_color = outline_color
        self.outline_w = outline_w

        self.rel_w, self.rel_h = rel_size

        self.x, self.y = pos

        self.rect = pygame.rect.Rect((0, 0), (0, 0))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self._circle_cache = {}
    
    def draw(self):
        if self.outline_w == 0:
            rendered_text = self.font.render(Config.current_local[self.text] if self.isLocal else self.text, True, self.color)
        else:
            rendered_text = self.render(Config.current_local[self.text] if self.isLocal else self.text, self.font, self.color, self.outline_color, self.outline_w)

        x = self.x if not (self.x == "center") else self.rel_w/2 - rendered_text.get_width()/2
        y = self.y if not (self.y == "center") else self.rel_h/2 - rendered_text.get_height()/2

        self.rect = pygame.rect.Rect(
            (x, y), 
            (rendered_text.get_width(), rendered_text.get_height())
        )

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.blit(rendered_text, (0, 0))
    
    def update(self, *events):
        self.draw()

    # ?? ???? ????????, ?????? ?????? ????????????????, ???? ?????? ?????????? ?????? ?????????????? ????????????

    def render(self, text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=0):
        textsurface = font.render(text, True, gfcolor).convert_alpha()
        w = textsurface.get_width() + 2 * opx
        h = font.get_height()

        osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

        for dx, dy in self._circlepoints(opx):
            surf.blit(osurf, (dx + opx, dy + opx))

        surf.blit(textsurface, (opx, opx))
        return surf

    def _circlepoints(self, r):
        r = int(round(r))
        if r in self._circle_cache:
            return self._circle_cache[r]
        x, y, e = r, 0, 1 - r
        self._circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points


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
    
    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        #?????????? ?????????? ??????????????, ?? ?????????????????? ?????????????????? ???????? ???????????? ??????, ?????????? ???????? ??????.
        mouse_pos = (mouse_pos[0] - self.rel_x, mouse_pos[1] - self.rel_y)

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.focused and event.button == 1:
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
        self.label = Label((self.slider.rect.width + 10, 0), self.get_percent(), False, 26, (Config.screen_width, Config.screen_height), (255, 255, 255), (0, 0, 0), 0, self.inner_group)

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
        self.inner_group.update(events)
        
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
                 on_selected_change=None, on_hover=None, on_hover_lose=None, *groups):
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
        self.currentOption = options[0] if len(options) > 0 else "??????????"
        self.on_selected_change = on_selected_change
        self.on_hover = on_hover
        self.on_hover_lose = on_hover_lose

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
        self.inner_group.update(events)

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.focused = True
            if self.on_hover is not None:
                self.on_hover()
        else:
            self.focused = False
            if self.on_hover_lose is not None:
                self.on_hover_lose()

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
                if event.button == 1:
                    self.selected = False
                    for opt in self.options:
                        if opt.isFocused():
                            tmp = self.currentOption
                            self.currentOption = opt.getText()
                            opt.setText(tmp)
                            options = [self.currentOption] + list(map(lambda x: x.getText(), self.options))
                            self.on_selected_change(options)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.focused and not self.selected:
                if event.button == 1:
                    self.selected = True

        self.draw()


class SaveSlot(pygame.sprite.Sprite):
    def __init__(self, pos, size, pic_size, screenshot_pic, outline_pic, date, on_click, *groups) -> None:
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size
        self.pic_size = pic_size
        self.pic_w, self.pic_h = pic_size

        self.screenshot_pic_data = screenshot_pic
        self.screenschot_pic = pygame.transform.scale(screenshot_pic, (self.pic_w-16, self.pic_h-16))
        self.outline_pic = pygame.transform.scale(outline_pic, pic_size)
        self.date = date
        self.on_click = on_click

        is_local = True if date == "??????????" else False
        self.desc_group = pygame.sprite.Group()
        self.date_label = Label(("center", self.pic_size[1]), date, is_local, 16, (self.w, self.h), (255, 255, 255), (0, 0, 0), 1, self.desc_group)

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

        self.active = False
        self.collided = False
        self.focused = False
        self.selected = False

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.screenschot_pic, (8, 8))
        self.image.blit(self.outline_pic, (0, 0))

        if self.active or (self.focused and not self.collided):
            pic_surf = pygame.Surface(self.pic_size, pygame.SRCALPHA, 32)
            pic_surf.fill((255, 255, 255, 128))
            self.image.blit(pic_surf, (0, 0))

        self.desc_group.draw(self.image)

    def update(self, *events):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.focused:
            self.focused = True
        elif not self.rect.collidepoint(mouse_pos) and self.focused:
            self.focused = False

        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.focused and not self.selected and not self.collided:
                    self.selected = True
                    self.on_click(self)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.selected:
                    self.selected = False

        self.draw()
        self.desc_group.update(*events)

    def set_collided(self, coll):
        self.collided = coll

    def set_active(self, act):
        self.active = act

    def set_screenshot(self, new_screenshot):
        self.screenschot_pic = new_screenshot
    
    def set_date(self, new_date):
        self.date = new_date
        self.date_label.text = new_date
        self.date_label.isLocal = True if self.date == "??????????" else False

    def is_void(self):
        return self.screenshot_pic_data == get_res("saves_void_save_pic")

class Picture(pygame.sprite.Sprite):
    def __init__(self, pos, size, pic, *groups) -> None:
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size
        self.pic = pygame.transform.scale(pic, size)

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.blit(self.pic, (0, 0))

    def update(self, *events):
        self.draw()

    def change_pic(self, new_pic):
        self.pic = pygame.transform.scale(new_pic, (self.w, self.h))