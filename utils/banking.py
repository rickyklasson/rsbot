from . import constants as cnst, input_util, vision_util, inventory_util
import time
import random
import mouse

# For now, assume we are close to a bank and can click on it directly.
def do_banking(img_offset: tuple):
    print('Banking...')
    click_point = vision_util.get_object_point(cnst.SCREEN_IMG_PATH, img_offset, cnst.BANK_COLOR)
    input_util.click_at(click_point, button='right')
    time.sleep(0.2)
    input_util.move_rel((random.uniform(-10, 10), random.randrange(38, 40)))
    mouse.click()
    time.sleep(15)
