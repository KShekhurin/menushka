from distutils.command.config import config
from Frames.Frames import *
from Inventory import Inventory
from Player import Player
from Item import *
from Pointer import PointerState
from Widgets import PictureButton
import Frames.MenuFrame as MenuFrame
import Frames.SaveMenuFrame as SaveMenuFrame
import os

class GameFrameData:
    def __init__(self, background_color, background_pic, player_pos, perspective, items_data):
        self.background_color = background_color
        self.background_pic = background_pic
        self.background_pic = pygame.transform.scale(background_pic, (Config.screen_width, Config.screen_height))
        self.player_pos = player_pos
        
        self.items_data = items_data

        self.perspective = perspective

class GameFrame(Frame):
    def __init__(self, id):
        super().__init__()

        self.id = id
        self.data = GameFrameData(*Config.scenes_data[id])
        self.items = []
        self.active_item = None

        self.player_pos = Settings.player_pos if Settings.last_scene_id == self.id and Settings.player_pos != (-1, -1) else self.data.player_pos

        self.is_controlable = True

        self.is_mouse_in_persp = False

        self.inventory_items = Settings.inventory_items

    def draw(self, screen):

        screen.fill(self.data.background_color)
        screen.blit(self.data.background_pic, (0, 0))
        self.item_group.draw(screen)

        super().draw(screen)

    def update(self, *events):
        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN: # this is mouse button click
                if event.button == 1:                # this is left mouse click
                    print(event.pos)

                    if self.helper.rect.collidepoint(event.pos):
                        pass
                    elif self.data.perspective.is_pos_in_perspective(event.pos) and self.is_controlable:
                        self.player.move_to(pygame.Vector2(event.pos))
                    elif not self.is_controlable and not self.inventory.is_focused():
                        self.inventory.close_inv()
                        self.is_controlable = True

        if self.is_controlable:
            self.item_group.update(events)

        mouse_pos = pygame.mouse.get_pos()
        if self.is_controlable:
            if self.data.perspective.is_pos_in_perspective(mouse_pos) and not self.is_mouse_in_persp:
                self.app.pointer.set_state(PointerState.WALK)
                self.is_mouse_in_persp = True
            elif not self.data.perspective.is_pos_in_perspective(mouse_pos) and self.is_mouse_in_persp:
                self.app.pointer.set_state(PointerState.DEFAULT)
                self.is_mouse_in_persp = False

        super().update(events)

    def show_tip(self, tip, is_pickable):
        self.tip_label.text = tip
        if is_pickable:
            self.app.pointer.set_state(PointerState.PICKUP)

    def clear_tip(self):
        self.tip_label.text = ""
        self.app.pointer.set_state(PointerState.DEFAULT)

    def goto_saves_menu(self):
        self.helper.save_blink_timer()
        self.save_state()

        self.app.reload_frame(SaveMenuFrame.SaveMenuFrame())

    def pickup_item(self, item, player_pos):
        if self.is_controlable:
            self.player.move_to(pygame.Vector2(player_pos), self.player.pickup_item)
            self.active_item = item

    def open_inventory(self):
        if self.is_controlable:
            self.inventory.open()
            self.is_controlable = False

    def add_item_to_inventory(self):
        self.inventory.put_item(self.active_item.id)
        self.inventory_items.append(self.active_item.id)
        self.active_item.delete()
        Settings.items_pickedup[self.id][self.items.index(self.active_item)] = True
        self.active_item = None
        self.app.pointer.set_state(PointerState.DEFAULT)
        self.clear_tip()

    def save_state(self):
        Settings.player_pos = self.player.get_pos()
        Settings.last_scene_id = self.id
        Settings.inventory_items = self.inventory_items
        pygame.image.save(self.app.screen, "tmp/screenshot.jpg")

    def post_init(self, app):
        super().post_init(app)

        self.game_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()

        self.player = Player(self.player_pos, (300, 300), self.data.perspective, self.add_item_to_inventory, self.game_group)
        self.tip_label = Label(("center", 560), "", False, 22, (Config.screen_width, Config.screen_height), (255,216,0), (0, 0, 0), 2, self.game_group)
        
        for i in range(0, len(self.data.items_data)):
            if Settings.items_pickedup[self.id][i]: continue
            item_id = self.data.items_data[i]
            self.items.append(Item(item_id, self.show_tip, self.clear_tip, self.pickup_item, None, self.item_group)) 

        self.inventory_btn = PictureButton((10, 10), (60, 70), "scene_open_inventory_btn_def_pic", "scene_open_inventory_btn_hover_pic", "Открыть инвентарь", self.open_inventory, self.show_tip, self.clear_tip, self.game_group)
        self.save_btn = PictureButton((90, 10), (60, 70), "scene_save_btn_def_pic", "scene_save_btn_hover_pic", "Сохраниться", self.goto_saves_menu, self.show_tip, self.clear_tip, self.game_group)

        self.inventory = Inventory(self.inventory_items, self.show_tip, self.clear_tip, self.game_group)

        self.append_many_widgets((self.game_group,))