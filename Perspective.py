class Perspective:
    def __init__(self):
        pass

    def get_scalar_by_cord(self, pos):
        pass

    def pos_in_persective(self, pos):
        pass

class WidePerspective(Perspective):
    def __init__(self, bottom, top, length):
        super().__init__()
        self.bottom, self.top = bottom, top
        self.length = length
        
    def get_scalar_by_cord(self, pos):
        super().get_scalar_by_cord(pos)
        
        scale_factor = 1 - abs(self.top - pos[1]) / self.length
        
        return scale_factor

    def pos_in_perspective(self, pos):
        super().pos_in_perspective(pos)

        return self.top > pos[1] > self.bottom
        

class TrapezoidPerspective(Perspective):
    def __init__(self, bottom, top, bottom_len, top_len):
        super().__init__()
        self.bottom, self.top = bottom, top
        self.bottom_len, self.top_len = bottom_len, top_len

    
