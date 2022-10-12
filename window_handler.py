import pyautogui as pg
import sys

def find_window(win_name: str):
    # Get titles of all active windows.
    window_titles = pg.getAllTitles()
    sought_title = None

    # Find Paint window.
    for t in window_titles:
        if win_name in t:
            sought_title = t
            break
    
    win = pg.getWindowsWithTitle(sought_title)[0]
    
    if win is None:
        print(f'Window with name "{win_name}" not found. Exiting!')
        sys.exit()
        
    return win