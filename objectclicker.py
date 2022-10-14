"""Autoclicker which records keystrokes and repeats actions"""
import argparse
from dataclasses import dataclass
import mouse
import random
import pyautogui as pg
import time
from utils import input_util, inventory_util, window_util, vision_util

SCREEN_IMG_PATH = 'tmp_img.png'
INV_IMG_PATH = 'tmp_inv.png'
BOUNDARY_COLOR = (255, 0, 250)
TIMEOUT_LIMIT = 15

@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

    def as_tuple(self):
        return (self.x, self.y, self.w, self.h)

def main(args):
    # Wait for user acknowledgement.
    input('Open your Runescape inventory then press ENTER to start')

    # Find window of interest.
    win = window_util.find_window(args.window)
    
    # Bring it into focus.
    win.minimize()
    win.restore()

    print(f'Window position: {win.box}')
    print(f'---- Open your inventory and click the top left corner of it. ----')
    inv_pos = input_util.wait_for_left_click()
    time.sleep(0.5)

    print(f'---- Click the bottom right corner of your inventory. ----')
    inv_botright = input_util.wait_for_left_click()
    inv_w = inv_botright[0] - inv_pos[0]
    inv_h = inv_botright[1] - inv_pos[1]
    inv_size = (inv_w, inv_h)

    inv = inventory_util.Inventory(inv_pos, inv_size)

    while inv.is_empty(27):
        # Take screenshot
        pg.screenshot(SCREEN_IMG_PATH, region=(win.box))

        # Find objects to click.
        points_to_click = vision_util.find_object_points(SCREEN_IMG_PATH, (win.box.left, win.box.top), BOUNDARY_COLOR)

        # Choose a random point to click.
        point = random.choice(points_to_click)
        pg.moveTo(point[0], point[1], 1, pg.easeOutQuad)
        mouse.click()
        
        timeout_timer = 0
        slot_to_fill = inv.first_empty
        while inv.first_empty == slot_to_fill:
            print(f'Waiting to fill slot: {slot_to_fill}')
            time.sleep(1)
            timeout_timer += 1
            if timeout_timer >= TIMEOUT_LIMIT:
                break
            inv.update_inv_status()
        
    print('Inventory full, exiting...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser('\n\nRun command example:\npython autoclicker.py --window RuneLite')
    
    # Required positional argument
    #parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    #parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-w", "--window", action="store", dest="window", type=str)

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    #parser.add_argument(
    #    "-v",
    #    "--verbose",
    #    action="count",
    #    default=0,
    #    help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    #parser.add_argument(
    #    "--version",
    #    action="version",
    #    version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)