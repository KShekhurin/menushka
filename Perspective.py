import math

class Perspective:
    def __init__(self):
        pass

    def get_scale_by_cord(self, pos):
        pass

    def is_pos_in_perspective(self, pos):
        pass

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

    
