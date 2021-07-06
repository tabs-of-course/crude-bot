from time import sleep
import sys
import random
from functions import *




def bot_thread(command_queue, thread_event):
    coordList = []
    x = 0
    y = 0
    w = 0
    h = 0

    window_name = 'LDPlayer'
    ooc_hp_pos = [276, 903] 
    ooc_mana_pos = [275, 916]
    attack_pos = [374, 729]


    hwnd = getSpecificHWND(window_name)

    window_list = []
    window_list = get_child_windows(hwnd)
    while True:

        # command response
        if not command_queue.empty():
            command = command_queue.get()

            if command == 'mouse pos':
                mouse_pos = current_mouse_pos(hwnd)
                try:
                    hwindc = win32gui.GetWindowDC(hwnd)
                    print(win32gui.GetPixel(
                        hwindc, mouse_pos[0], mouse_pos[1]))
                    print('[',mouse_pos[0],', ',mouse_pos[1],']',sep='')
                except:
                    print('Out of bounds')

            if command == 'command':
                mobs_pos = []
                while(len(mobs_pos) < 3):
                    mobs_pos = find_diff(hwnd)
                    for index, c in enumerate(mobs_pos):
                        x, y, h, w = c
                        print(index, ':', c)

            if command == 'get hwnd':

                hwnd = getSpecificHWND(window_name)
                print('Window handle:', hwnd)
                window_list = []
                window_list = get_child_windows(hwnd)

                for (index, value) in enumerate(window_list):
                    print(index, value)
                

            if command == 'exit':
                sys.exit(0)

        # event response
        if thread_event.is_set():
            sleep(0.5)
            mobs_pos = []
            x = 0
            y = 0
            w = 0
            h = 0
            x_item = 0
            y_item = 0
            x_continue = 0
            y_continue = 0
            x_back = 0
            y_back = 0

            in_map = False
            in_menu = False
            in_combat = False
            need_to_click_continue = False

            # check if we are in combat
            x_item, y_item = find_sprite(hwnd, 'sprites/item.jpg')
            if x_item != 0 and y_item != 0:
                in_combat = True

            # check if we need to click continue
            x_continue, y_continue = find_sprite(hwnd, 'sprites/continue.jpg')
            if x_continue != 0 and y_continue != 0:
                need_to_click_continue = True

            # check if we are in the map window
            x_ooc, y_ooc = find_sprite(hwnd, 'sprites/ooc.jpg')
            if x_ooc != 0 and y_ooc != 0:
                in_map = True

            # check if we got stuck
            x_back, y_back = find_sprite(hwnd, 'sprites/back.jpg')
            if x_back != 0 and y_back != 0:
                in_menu = True

            if in_menu is True:
                left_click(window_list[0], x_back, y_back, 0.1)

            # find enemy on map
            if in_map is True:
                print('Out of combat')
                try:
                    hwindc = win32gui.GetWindowDC(hwnd)
                    hp_status_ooc = win32gui.GetPixel(hwindc, ooc_hp_pos[0],ooc_hp_pos[1])
                    mana_status_ooc = win32gui.GetPixel(hwindc, ooc_mana_pos[0],ooc_mana_pos[1])
                except:
                    print('Hp and Mana check error')

                if hp_status_ooc not in range(650000, 730000, 1) or mana_status_ooc not in range(16600000, 16800000, 1):
                    print('Healing')
                    left_click(window_list[0], x_ooc, y_ooc, 1.2)
                    continue

                mobs_pos = find_diff(hwnd)
                for index, c in enumerate(mobs_pos):
                    x, y, w, h = c
                    print(index, ':', c)
                try:
                    x, y, w, h = random.choice(mobs_pos)
                except:
                    print('No mobs found')

            # battle random enemy
            if x and y != 0:
                print('Enganging enemy at:', x, y)
                left_click(window_list[0], x + int(w/2), y + int(h/2), 1.2)

            # combat loop
            if in_combat is True:
                print("Attacking")
                for x_pos in range(attack_pos[0], attack_pos[0]+12, 3):
                    left_click(window_list[0], x_pos, attack_pos[1], 0.1)
                    sleep(0.1)

            if need_to_click_continue is True:
                print('Clicking continue')
                left_click(window_list[0], x_continue, y_continue, 0.1)
