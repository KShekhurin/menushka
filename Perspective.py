import math

import pygame

class Perspective:
    def __init__(self):
        self.is_debug = False

    def get_scale_by_cord(self, pos):
        pass

    def is_pos_in_perspective(self, pos):
        pass

    def draw_view(self, screen):
        #Только для тестов перспективы! 
        # Функция рисует поверх всего и ей глубоко насрать.
        pass


class PerspectiveSetter:
    def __init__(self, point, bot_l_pos, bot_r_pos):
        self.point_pos = point
        self.bot_l_pos = bot_l_pos
        self.bot_r_pos = bot_r_pos
    
    def calculate_scaling(self, pos):
        

        return 1 / (1 - (pos[1] - self.bot_l_pos[1]) / (self.bot_l_pos[1] - self.point_pos[1])) 


class CustomPerspective(Perspective):
    def __init__(self, setter: PerspectiveSetter, points):
        super().__init__()

        self.perspective_setter = setter
        self.points = points
    
    def is_pos_in_perspective(self, pos):
        p = self.points
        result = False
        j = len(p) - 1
        for i in range(len(p)):
            if ((p[i][1] < pos[1] and p[j][1] >= pos[1] or p[j][1] < pos[1] and p[i][1] >= pos[1]) and
                 (p[i][0] + (pos[1] - p[i][1]) / (p[j][1] - p[i][1]) * (p[j][0] - p[i][0]) < pos[0])):
                result = not result
            j = i
        return result

    def get_scale_by_cord(self, pos):
        return self.perspective_setter.calculate_scaling(pos)
    
    def draw_view(self, screen):
        surface = pygame.Surface((800, 600))
        surface.set_alpha(128)

        pygame.draw.polygon(
            surface, (255, 0, 0),
            (self.perspective_setter.point_pos,
            self.perspective_setter.bot_l_pos,
            self.perspective_setter.bot_r_pos)
        )

        screen.blit(surface, (0, 0))

        pygame.draw.lines(screen,
            (255, 255, 255), True,
            self.points
        )        

class RectPerspective(Perspective):
    def __init__(self, bottom, top, left, right):
        super().__init__()
        self.bottom, self.top = bottom, top
        self.left, self.right = left, right
        self.length = self.right - self.left
        
    def get_scale_by_cord(self, pos):
        super().get_scale_by_cord(pos)
        
        scale_factor = 1 - abs(pos[1] - self.top) / self.length
        #scale_factor = 1
        
        return scale_factor

    def is_pos_in_perspective(self, pos):
        super().is_pos_in_perspective(pos)

        return (self.top <= pos[1] <= self.bottom) and (self.right >= pos[0] >= self.left)
        

class TrapezoidPerspective(Perspective):
    def __init__(self, bottom, top, bottom_left, bottom_right, top_left, top_right):
        super().__init__()
        self.bottom, self.top = bottom, top
        self.bottom_left, self.bottom_right = bottom_left, bottom_right
        self.top_left, self.top_right = top_left, top_right
        self.bottom_length = self.bottom_right - self.bottom_left
        self.top_length = self.top_right - self.top_left

    def get_scale_by_cord(self, pos):
        super().get_scale_by_cord(pos)

        # нвахожу длину линии, на которой находится pos
        bottom_length_part = (self.bottom_length - self.top_length) / 2
        pos_length_part = (bottom_length_part * (pos[1] - self.top)) / (self.bottom - self.top)
        pos_length = pos_length_part * 2 + self.top_length

        scale = pos_length / self.bottom_length

        return scale

    def is_pos_in_perspective(self, pos):
        super().is_pos_in_perspective(pos)

        bottom_length_part = (self.bottom_length - self.top_length) / 2
        pos_length_part_bottom = (bottom_length_part * (self.bottom - pos[1])) / (self.bottom - self.top)

        pos_left = self.bottom_left + pos_length_part_bottom
        pos_right = self.bottom_right - pos_length_part_bottom

        return (self.top <= pos[1] <= self.bottom) and (pos_right >= pos[0] >= pos_left)

    
