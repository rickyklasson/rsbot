import cv2
import mouse
import numpy as np
import random
import pyautogui as pg
import time
from . import input_util
from dataclasses import dataclass


INV_IMG_PATH = 'tmp_img.png'
NR_INV_SLOTS = 28

@dataclass
class InvItem:
    idx: int
    pos: tuple
    empty: bool
    preserve: bool

@dataclass
class Inventory:
    pos: tuple
    size: tuple
    item_size: tuple
    items: list[InvItem]
    first_empty: int

    def __init__(self, pos: tuple, bottom_right: tuple, items_to_preserve: list):
        print('Initializing inventory model')
        inv_w = bottom_right[0] - pos[0]
        inv_h = bottom_right[1] - pos[1]

        self.items = []
        self.pos = pos
        self.size = (inv_w, inv_h)
        self.first_empty = 0

        slot_w = self.size[0] // 4
        slot_h = self.size[1] // 7
        self.item_size = (slot_w, slot_h)

        print(f'Inventory pos: {pos}, size: {self.size}')

        # 28 inventory slots in 4x7 grid.
        for vert in range(0, 7):
            for hori in range(0, 4):
                item_idx = vert * 4 + hori
                item_pos = (self.pos[0] + hori * slot_w, self.pos[1] + vert * slot_h)
                preserve_item = item_idx in items_to_preserve
                inv_item = InvItem(item_idx, item_pos, empty=False, preserve=preserve_item)

                self.items.append(inv_item)
        
        for i in range(NR_INV_SLOTS):
            self.items[i].empty = self.is_empty(i)
        
        self.update_first_empty()

        print(f'Initialized inventory. First empty slot is slot {self.first_empty}')
    
    def is_empty(self, item_idx: int):
        print(f'Checking if slot {item_idx} is empty...')
        x, y = self.items[item_idx].pos
        w, h = self.item_size
        pg.screenshot(INV_IMG_PATH, region=(x, y, w, h))

        img = cv2.imread(INV_IMG_PATH)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        variance = np.var(gray)

        if variance < 1:
            return True
        else:
            return False

    def got_new_item(self):
        # Return true if first empty slot is no longer empty.
        if self.is_empty(self.first_empty):
            return False
        else:
            self.items[self.first_empty].empty = False
            return True

    def update_inv_status(self):
        for i in range(NR_INV_SLOTS):
            self.items[i].empty = self.is_empty(i)
        self.update_first_empty()

        # Debug print.
        print(f'------ INVENTORY STATUS ------')
        inv_str = ''
        for i in range(NR_INV_SLOTS):
            if i % 4 == 0:
                inv_str += '\n'
            inv_str += str(self.items[i].empty) + ' '
        print(inv_str)
        print('------')

    def update_first_empty(self):
        for i in range(NR_INV_SLOTS):
            if self.items[i].empty:
                self.first_empty = i
                break
    
    def drop_item(self, item_idx: int):
        # Don't drop preserved items.
        if self.items[item_idx].preserve:
            return

        print(f'Dropping item with idx {item_idx}')
        # Find item pos.
        item_pos = self.items[item_idx].pos

        # Find center of item rect.
        x_center = int(item_pos[0] + self.item_size[0] / 2)
        y_center = int(item_pos[1] + self.item_size[1] / 2)

        # Small random offset.
        x_click = x_center + random.randint(-6, 6)
        y_click = y_center + random.randint(-6, 6)

        # Move mouse to pos.
        input_util.move_to((x_click, y_click))
        mouse.right_click()

        # Move to drop.
        rel_x = random.randint(-10, 10)
        rel_y = random.randint(33, 38)
        input_util.move_rel((rel_x, rel_y))
        mouse.click()
        time.sleep(0.1)

        # Verify dropped.
        self.items[item_idx].empty = self.is_empty(item_idx)

    def drop_all(self):
        # Check what item slots are non-empty.
        idxs = [i for i in range(NR_INV_SLOTS) if not self.items[i].empty]
        random.shuffle(idxs)

        for i in idxs:
            self.drop_item(i)

    def deposit_all(self):
        item_pos = self.items[1].pos

        # Find center of item rect.
        x_center = int(item_pos[0] + self.item_size[0] / 2)
        y_center = int(item_pos[1] + self.item_size[1] / 2)

        # Small random offset.
        x_click = x_center + random.randint(-6, 6)
        y_click = y_center + random.randint(-6, 6)

        # Move mouse to pos.
        input_util.move_to((x_click, y_click))
        mouse.right_click()

        # Move to drop.
        rel_x = random.randint(-10, 10)
        rel_y = random.randint(84, 88)
        input_util.move_rel((rel_x, rel_y))
        mouse.click()
        time.sleep(0.1)
        input_util.click_at((1075, 114))

        