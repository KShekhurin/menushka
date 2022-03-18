import pygame
from Utils.Assets import get_res
from Item import *

class InventoryItem(pygame.sprite.Sprite):
    def __init__(self, pos, id, *groups):
        super().__init__(*groups)

        self.id = id
        self.x, self.y = pos
        self.size, self.pic, self.tip = Config.inventory_items_ids[id]
        self.pic = pygame.transform.scale(self.pic, self.size)

        self.rect = pygame.rect.Rect((self.x, self.y), self.size)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)

    def draw(self):
        self.image.blit(self.pic, (0, 0))

    def update(self, *events):
        self.draw()

class InventorySlot(pygame.sprite.Sprite):
    def __init__(self, pos, size, item_id, on_focus, on_lose_focus, on_click, *groups):
        super().__init__(*groups)

        self.x, self.y = pos
        self.w, self.h = size
    
        self.on_focus = on_focus
        self.on_lose_focus = on_lose_focus
        self.on_click = on_click

        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

        self.focused = False

        self.contain_group = pygame.sprite.Group()
        if item_id is not None:
            self.contain = InventoryItem((self.w//2 - Config.inventory_items_ids[item_id][0][0]//2, self.h//2 - Config.inventory_items_ids[item_id][0][1]//2), item_id, self.contain_group)
        else:
            self.contain = None

    def draw(self):
        #print(self.image.get_rect().x)
        #self.image.fill((0, 0, 0))

        if self.focused or self.contain is not None:
            self.image.fill((255, 255, 255, 128))
        else:
            self.image.fill((0, 0, 0, 0))

        if self.contain is not None:
            self.contain_group.draw(self.image)

    def update(self, *events):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= 185
        mouse_y -= 50
        #print(mouse_pos, self.rect.x, self.rect.y)
        if self.rect.collidepoint((mouse_x, mouse_y)) and not self.focused:
            self.focused = True
            if self.on_focus is not None and self.contain is not None:
                self.on_focus(self.contain.tip, False)
        elif not self.rect.collidepoint((mouse_x, mouse_y)) and self.focused:
            self.focused = False
            if self.on_lose_focus is not None and self.contain is not None:
                self.on_lose_focus()

        self.draw()
        self.contain_group.update()

    def put(self, item_id):
        self.contain = InventoryItem((self.w//2 - Config.inventory_items_ids[item_id][0][0]//2, self.h//2 - Config.inventory_items_ids[item_id][0][1]//2), item_id, self.contain_group)

    def is_empty(self):
        return self.contain is None

class Inventory(pygame.sprite.Sprite):
    def __init__(self, items_ids, on_slot_focus, on_slot_lose_focus, *groups):
        super().__init__(*groups)

        self.pos = (185, 50)
        self.size = (430, 500)

        self.background_pic = pygame.transform.scale(get_res("inventory_background_pic"), self.size)

        self.rect = pygame.rect.Rect(self.pos, self.size)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)

        self.is_opened = False
        self.focused = False

        self.max_len = 2

        _items = [*items_ids] if len(items_ids) > 0 else []
        for i in range(0, self.max_len-len(items_ids)): _items.append(None)

        self.slots_group = pygame.sprite.Group()
        self.slots = (
            InventorySlot((250-185, 198-50), (315-250, 252-198), _items[0], on_slot_focus, on_slot_lose_focus, None, self.slots_group),
            InventorySlot((476-185, 181-50), (538-476, 249-181), _items[1], on_slot_focus, on_slot_lose_focus, None, self.slots_group),
        )

        self.full_slots = len(items_ids)

    def open(self):
        self.is_opened = True

    def close_inv(self):
        self.is_opened = False

    def is_focused(self):
        return self.focused

    def put_item(self, item):
        self.slots[self.full_slots].put(item)
        self.full_slots += 1

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        if self.is_opened:
            self.image.blit(self.background_pic, (0, 0))

            self.slots_group.draw(self.image)

    def update(self, *events):
        if self.is_opened:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos) and not self.focused:
                self.focused = True
            elif not self.rect.collidepoint(mouse_pos) and self.focused:
                self.focused = False

            self.slots_group.update()

        self.draw()