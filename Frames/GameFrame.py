from Frames.Frames import *
from Inventory import Inventory
from NPC import NPC
from Player import Player
from Item import *
from Pointer import PointerState
from Portal import Portal
from Widgets import PictureButton
import Frames.MenuFrame as MenuFrame
import Frames.SaveMenuFrame as SaveMenuFrame
import Frames.DialogueFrame as DialogueFrame
import os

class GameFrameData:
    def __init__(self, background_color, background_pic, player_pos, perspective, items_loc_data, portals_loc_data, npcs_loc_data):
        self.background_color = background_color
        self.background_pic = get_res(background_pic)
        self.background_pic = pygame.transform.scale(self.background_pic, (Config.screen_width, Config.screen_height))
        self.player_pos = player_pos
        
        self.items_data = items_loc_data
        self.portals_data = portals_loc_data
        self.npcs_data = npcs_loc_data

        self.perspective = perspective

class GameFrame(Frame):
    def __init__(self, id):
        super().__init__()

        self.id = id
        self.data = GameFrameData(*Config.scenes_data[id])
        self.data.perspective.is_debug = True
        self.items = []
        self.portals = []
        self.npcs = []
        self.active_portal = None
        self.active_item = None
        self.saved_dialogue_id = ""

        self.player_pos = Settings.player_pos if Settings.last_scene_id == self.id and Settings.player_pos != (-1, -1) else self.data.player_pos

        self.is_controlable = True

        self.is_mouse_in_persp = False
        self.smth_focused = False

        self.inventory_items = Settings.inventory_items

    def draw(self, screen):

        screen.fill(self.data.background_color)
        screen.blit(self.data.background_pic, (0, 0))

        if self.data.perspective.is_debug:
            self.data.perspective.draw_view(screen)

        self.item_group.draw(screen)
        self.npc_group.draw(screen)
        self.player_group.draw(screen)

        super().draw(screen)

    def update(self, *events):
        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN: # this is mouse button click
                if event.button == 1:                # this is left mouse click
                    print(event.pos)
                    pos_scale = self.data.perspective.get_scale_by_cord(event.pos)

                    if self.helper.rect.collidepoint(event.pos):
                        pass
                    elif self.data.perspective.is_pos_in_perspective((event.pos[0] + (self.player.w*pos_scale)//2, event.pos[1])) and self.data.perspective.is_pos_in_perspective((event.pos[0] - (self.player.w*pos_scale)//2, event.pos[1])) and self.is_controlable:
                        self.player.move_to(pygame.Vector2((event.pos[0] + self.app.pointer.w//2, event.pos[1] + self.app.pointer.h//2)))
                    elif not self.is_controlable and not self.inventory.is_focused():
                        self.inventory.close_inv()
                        self.is_controlable = True
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.app.pointer.set_state(PointerState.DEFAULT)
                dialogue_data = DialogueFrame.DialogueFrameData(get_res("dialogue_meadow_background_pic"), "zhirik", "zhirik_0")
                self.app.reload_frame(DialogueFrame.DialogueFrame(dialogue_data))

        mouse_pos = pygame.mouse.get_pos()
        if self.is_controlable:
            pos_scale = self.data.perspective.get_scale_by_cord(mouse_pos)
            if self.data.perspective.is_pos_in_perspective((mouse_pos[0] + (self.player.w*pos_scale)//2, mouse_pos[1])) and self.data.perspective.is_pos_in_perspective((mouse_pos[0] - (self.player.w*pos_scale)//2, mouse_pos[1])) and not self.is_mouse_in_persp and not self.smth_focused:
                self.app.pointer.set_state(PointerState.WALK)
                self.is_mouse_in_persp = True
            elif not (self.data.perspective.is_pos_in_perspective((mouse_pos[0] + (self.player.w*pos_scale)//2, mouse_pos[1])) and self.data.perspective.is_pos_in_perspective((mouse_pos[0] - (self.player.w*pos_scale)//2, mouse_pos[1]))) and self.is_mouse_in_persp and not self.smth_focused:
                self.app.pointer.set_state(PointerState.DEFAULT)
                self.reset_focuses()

        if self.is_controlable:
            self.item_group.update(events)
            self.npc_group.update(events)

        self.player_group.update(events)

        super().update(events)

    def show_tip(self, tip, cursor_state):
        self.tip_label.text = tip
        self.app.pointer.set_state(cursor_state)
        self.smth_focused = True

    def clear_tip(self):
        self.tip_label.text = ""
        self.app.pointer.set_state(PointerState.DEFAULT)
        self.reset_focuses()

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

    def goto_portal(self, dest_id):
        if self.is_controlable:
            mouse_pos = pygame.mouse.get_pos()
            self.player.move_to(pygame.Vector2((mouse_pos[0] + self.app.pointer.w//2, mouse_pos[1] + self.app.pointer.h//2)), self.goto_another_scene)
            self.active_portal = dest_id

    def goto_another_scene(self):
        self.app.reload_frame(GameFrame(self.active_portal))

    def speak(self, player_pos, dialogue_id):
        if self.is_controlable:
            self.player.move_to(pygame.Vector2(player_pos), self.goto_dialogue)
            self.saved_dialogue_id = dialogue_id

    def goto_dialogue(self):
        self.save_state()

        dialogue_data = DialogueFrame.DialogueFrameData(get_res("dialogue_meadow_background_pic"), self.saved_dialogue_id)
        self.app.reload_frame(DialogueFrame.DialogueFrame(dialogue_data))

    def save_state(self):
        Settings.player_pos = self.player.get_pos()
        Settings.last_scene_id = self.id
        Settings.inventory_items = self.inventory_items
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        pygame.image.save(self.app.screen, "tmp/screenshot.jpg")

    def reset_focuses(self):
        self.is_mouse_in_persp = False
        self.smth_focused = False
        self.player.focused = False
        self.helper.focused = False
        self.inventory_btn.focused = False
        self.save_btn.focused = False
        for item in self.items: item.focused = False
        for portal in self.portals: portal.focused = False
        for npc in self.npcs: npc.focused = False

    def post_init(self, app):
        super().post_init(app)

        self.helper_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.gui_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.portals_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()

        self.helper = Helper((0, Config.screen_height - 200), (200, 200), self.helper_group)

        self.player = Player(self.player_pos, (160, 300), self.data.perspective, self.add_item_to_inventory, self.player_group)
        self.tip_label = Label(("center", 560), "", False, 22, (Config.screen_width, Config.screen_height), (255,216,0), (0, 0, 0), 2, self.gui_group)
        
        for i in range(0, len(self.data.items_data)):
            if Settings.items_pickedup[self.id][i]: continue
            item_data = self.data.items_data[i]
            self.items.append(Item(item_data, self.show_tip, self.clear_tip, self.pickup_item, None, self.item_group))
        
        for i in range(0, len(self.data.portals_data)):
            portal_data = self.data.portals_data
            self.portals.append(Portal(*portal_data, self.show_tip, self.clear_tip, self.goto_portal, self.portals_group))

        for i in range(0, len(self.data.npcs_data)):
            npc_loc_data = self.data.npcs_data
            npc_id = npc_loc_data[0]
            npc_data = Config.npcs_data[npc_id]
            self.npcs.append(NPC(*npc_loc_data[1:], get_res(npc_data[0]), npc_data[1], self.show_tip, self.clear_tip, self.speak, self.npc_group))

        self.inventory_btn = PictureButton((10, 10), (60, 70), "scene_open_inventory_btn_def_pic", "scene_open_inventory_btn_hover_pic", "?????????????? ??????????????????", self.open_inventory, self.show_tip, self.clear_tip, self.gui_group)
        self.save_btn = PictureButton((90, 10), (60, 70), "scene_save_btn_def_pic", "scene_save_btn_hover_pic", "??????????????????????", self.goto_saves_menu, self.show_tip, self.clear_tip, self.gui_group)

        self.inventory = Inventory(self.inventory_items, self.show_tip, self.clear_tip, self.gui_group)

        self.append_many_widgets((self.gui_group, self.portals_group, self.helper_group))