from Frames.Frames import *
from Player import Player
from Item import *
from Pointer import PointerState

class GameFrameData:
    def __init__(self, background_color, background_pic, player_pos, items_data):
        self.background_color = background_color
        self.background_pic = background_pic
        self.background_pic = pygame.transform.scale(background_pic, (Config.screen_width, Config.screen_height))
        self.player_pos = player_pos
        
        self.items_data = items_data

class GameFrame(Frame):
    def __init__(self, data: GameFrameData):
        super().__init__()

        self.data = data
        self.items = []

    def draw(self, screen):
        screen.fill(self.data.background_color)
        screen.blit(self.data.background_pic, (0, 0))

        super().draw(screen)

    def update(self, *events):
        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN: # this is mouse button click
                if event.button == 1:                # this is left mouse click
                    if self.helper.rect.collidepoint(event.pos):
                        pass
                    else:
                        self.player.move_to(pygame.Vector2(event.pos))
                        print(event.pos)

        super().update(events)

    def show_tip(self, tip):
        self.tip_label.text = tip
        self.app.pointer.set_state(PointerState.PICKUP)

    def clear_tip(self):
        self.tip_label.text = ""
        self.app.pointer.set_state(PointerState.DEFAULT)

    def post_init(self, app):
        super().post_init(app)

        self.game_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()

        self.player = Player(self.data.player_pos, (200, 200), self.game_group)
        self.tip_label = Label(("center", 560), "", False, 22, (255,216,0), (0, 0, 0), 2, self.game_group)
        
        for item_data in self.data.items_data:
           self.items.append(Item(item_data, self.show_tip, self.clear_tip, self.item_group)) 

        self.append_many_widgets((self.item_group, self.game_group,))