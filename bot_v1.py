"""Autoclicker which records keystrokes and repeats actions"""
import argparse
from dataclasses import dataclass
import mouse
import random
import pyautogui as pg
import time
from utils import banking, constants as cnst, input_util, inventory_util, window_util, vision_util

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
    print(f'---- Click the top left corner of your inventory. ----')
    inv_pos = input_util.record_next_left_click()
    time.sleep(0.8)

    print(f'---- Click the bottom right corner of your inventory. ----')
    inv_botright = input_util.record_next_left_click()

    inv = inventory_util.Inventory(inv_pos, inv_botright, args.preserve)
    
    # Main botting loop.
    while True:
        # Check if inventory is full. Bank or drop if it is.
        # Also drop all a small percentage of the time.
        if not inv.is_empty(inventory_util.NR_INV_SLOTS - 1):
            # Banking
            if args.banking:
                pg.screenshot(cnst.SCREEN_IMG_PATH, region=(win.box.left, win.box.top, win.box.width - 200, win.box.height - 40))
                banking.do_banking((win.box.left, win.box.top))
                inv.deposit_all()
            # Dropping
            else:
                inv.drop_all()
        
            # Sleep for some time between rotations.
            sleep_time = random.randint(1, 10)
            print(f'Sleeping for {sleep_time}s before next rotation')
            time.sleep(sleep_time)
        
        # Analyse objects in window.
        print('Analyzing screen content')
        pg.screenshot(cnst.SCREEN_IMG_PATH, region=(win.box.left, win.box.top, win.box.width - 200, win.box.height - 40))

        # Find object to click.
        click_coord = vision_util.get_object_point(cnst.SCREEN_IMG_PATH, (win.box.left, win.box.top), cnst.OBJECT_COLOR)

        if click_coord is None:
            time.sleep(3)
            continue

        # Choose a random point to click.
        print('Choosing action')
        input_util.move_to(click_coord)
        mouse.click()
        
        timeout_timer = 0
        slot_to_fill = inv.first_empty
        
        print(f'Waiting to fill slot: {slot_to_fill}')
        
        # Update inventory status before checking for item.
        inv.update_inv_status()

        # Wait for next empty slot to fill.
        while not inv.got_new_item():
            time.sleep(3)
            timeout_timer += 3
            if timeout_timer >= cnst.TIMEOUT_LIMIT:
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser('\n\nRun command example:\npython autoclicker.py --window RuneLite')
    
    # Required positional argument
    #parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    #parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Which window to focus.
    parser.add_argument("-w", "--window", action="store", type=str, required=True)

    parser.add_argument("-b", "--banking", action="store_true")

    parser.add_argument('-p','--preserve', nargs='+', type=int, help='List of inventory indexes to not drop.', required=False, default=[])



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