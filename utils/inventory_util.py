import cv2
import numpy as np
import pyautogui as pg
from dataclasses import dataclass

INV_IMG_PATH = 'tmp_img.png'
NR_INV_SLOTS = 28

@dataclass
class InvItem:
    idx: int
    pos: tuple
    empty: bool

@dataclass
class Inventory:
    pos: tuple
    size: tuple
    item_size: tuple
    items: list[InvItem]
    first_empty: int

    def __init__(self, pos: tuple, size: tuple):
        self.items = []
        self.pos = pos
        self.size = size
        self.first_empty = 0

        slot_w = self.size[0] // 4
        slot_h = self.size[1] // 7
        self.item_size = (slot_w, slot_h)

        print(f'Inventory pos: {pos}, size: {size}')

        # 28 inventory slots in 4x7 grid.
        for vert in range(0, 7):
            for hori in range(0, 4):
                item_idx = vert * 4 + hori
                item_pos = (self.pos[0] + hori * slot_w, self.pos[1] + vert * slot_h)
                inv_item = InvItem(item_idx, item_pos, False)

                self.items.append(inv_item)
        
        for i in range(NR_INV_SLOTS):
            self.items[i].empty = self.is_empty(i)
        
        self.update_first_empty()

        print(f'Initialized inventory with items: {self.items}')
    
    def is_empty(self, item_idx: int):
        x, y = self.items[item_idx].pos
        w, h = self.item_size
        img_path = f'item_{item_idx}_tmp_img.png'
        pg.screenshot(img_path, region=(x, y, w, h))

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        variance = np.var(gray)

        if variance < 1:
            return True
        else:
            return False

    def update_inv_status(self):
        for i in range(NR_INV_SLOTS):
            self.items[i].empty = self.is_empty(i)
        self.update_first_empty()

    def update_first_empty(self):
        for i in range(NR_INV_SLOTS):
            if self.items[i].empty:
                self.first_empty = i
                break