from Frames.Frames import *
from Player import Player

class GameFrameData:
    def __init__(self, background_color, background_pic, player_pos):
        self.background_color = background_color
        self.background_pic = background_pic
        self.background_pic = pygame.transform.scale(background_pic, (Config.screen_width, Config.screen_height))
        self.player_pos = player_pos

class GameFrame(Frame):
    def __init__(self, data: GameFrameData):
        super().__init__()

        self.data = data

    def draw(self, screen):
        screen.fill(self.data.background_color)
        screen.blit(self.data.background_pic, (0, 0))

        super().draw(screen)

    def update(self, *events):
        super().update(*events)

    def post_init(self, app):
        super().post_init(app)

        self.game_group = pygame.sprite.Group()

        self.player = Player(self.data.player_pos, (200, 200), self.game_group)

        self.append_many_widgets((self.game_group,))