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
    def __init__(self, bottom, top, bottom_len, top_len):
        super().__init__()
        self.bottom, self.top = bottom, top
        self.bottom_len, self.top_len = bottom_len, top_len

    
