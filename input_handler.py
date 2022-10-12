from dataclasses import dataclass
import tempfile
from tkinter import LEFT
import keyboard
import mouse
import pyautogui as pg
import time

@dataclass
class MouseInput:
    pos_x: int
    pos_y: int
    left_clicked: bool
    timestamp: float

def record_mouse_input() -> list:
    # Record list of mouse input.
    recorded_mouse_input = [] 
    start_time = time.time()
    elapsed_time = 0

    while True:
        pos_x, pos_y = mouse.get_position()
        left_clicked = mouse.is_pressed(button='left')
        new_input = MouseInput(pos_x, pos_y, left_clicked, elapsed_time)
        recorded_mouse_input.append(new_input)
        print(new_input)
        
        if keyboard.is_pressed('x'):
            break
        
        elapsed_time = time.time() - start_time
    
    return recorded_mouse_input

def filter_clicks(raw_input: list) -> list:
    filt_inputs = []
    
    last_was_clicked = False

    # Filter out click locations.
    for mouse_input in raw_input:
        if mouse_input.left_clicked and not last_was_clicked:
            filt_inputs.append(mouse_input)
        last_was_clicked = mouse_input.left_clicked

    print(f'---- Filtered out the following {len(filt_inputs)} inputs ----')
    for f in filt_inputs:
        print(f)

    return filt_inputs

def replay_inputs(inputs: list):
    # Wait 1.5x delay before replaying mouse inputs.
    while True:
        last_time = 0
        for mouse_input in inputs:
            time_to_next = mouse_input.timestamp - last_time
            last_time = mouse_input.timestamp
            print(f'Sleeping for {time_to_next}')
            time.sleep(time_to_next)
            print(f'Moving mouse to ({mouse_input.pos_x}, {mouse_input.pos_y})')
            pg.moveTo(mouse_input.pos_x, mouse_input.pos_y, 1, pg.easeOutQuad)
            time.sleep(1.2)
            print('Clicking...')
            mouse.click()