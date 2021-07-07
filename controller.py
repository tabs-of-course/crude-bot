from time import sleep
import sys
import random

from numpy.core.fromnumeric import var
from functions import *


def bot_thread(command_queue, thread_event):
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

    window_name = 'LDPlayer'

    ooc_hp_pos = [297, 970]
    ooc_mana_pos = [298, 987]
    attack_pos = [387, 791]

    hwnd = getSpecificHWND(window_name)

    window_list = []
    window_list = get_child_windows(hwnd)
    while True:
        sleep(0.1)
        # Command response
        if not command_queue.empty():
            command = command_queue.get()

            if command == 'mouse pos':
                mouse_pos = current_mouse_pos(hwnd)
                try:
                    hwindc = win32gui.GetWindowDC(hwnd)
                    print(win32gui.GetPixel(
                        hwindc, mouse_pos[0], mouse_pos[1]))
                    print('[', mouse_pos[0], ', ', mouse_pos[1], ']', sep='')
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

        # Event response
        if thread_event.is_set():
            sleep(0.4)
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

            mobs_pos = []

            # Check if we are in combat
            x_item, y_item = find_sprite(hwnd, 'sprites/item.jpg')
            if x_item != 0 and y_item != 0:
                in_combat = True

            # Check if we need to click continue
            x_continue, y_continue = find_sprite(hwnd, 'sprites/continue.jpg')
            if x_continue != 0 and y_continue != 0:
                need_to_click_continue = True

            # Check if we are in the map window
            x_ooc, y_ooc = find_sprite(hwnd, 'sprites/ooc.jpg')
            if x_ooc != 0 and y_ooc != 0:
                in_map = True

            # Check if we got stuck
            x_back, y_back = find_sprite(hwnd, 'sprites/back.jpg')
            if x_back != 0 and y_back != 0:
                in_menu = True

            if in_menu is True:
                left_click(window_list[0], x_back, y_back, 0.1)

            # Find enemy on map
            if in_map is True:
                
                try:
                    hwindc = win32gui.GetWindowDC(hwnd)
                    hp_status_ooc = win32gui.GetPixel(
                        hwindc, ooc_hp_pos[0], ooc_hp_pos[1])
                    mana_status_ooc = win32gui.GetPixel(
                        hwindc, ooc_mana_pos[0], ooc_mana_pos[1])
                except:
                    print('Hp and Mana check error')

                if hp_status_ooc not in range(650000, 730000, 1) or mana_status_ooc not in range(16600000, 16800000, 1):
                    print('Healing')
                    left_click(window_list[0], x_ooc, y_ooc, 1.2)
                    continue
                
                print('Searchin for enemies')
                while(len(mobs_pos)< 2):
                    mobs_pos = find_diff(hwnd)
                # for index, c in enumerate(mobs_pos):
                #     x, y, w, h = c
                #     print(index, ':', c)
                try:
                    x, y, w, h = random.choice(mobs_pos)
                except:
                    print('No mobs found')

            # Battle random enemy
            if x and y != 0:
                # print('Engaging enemy at:', x, y)
                print('Trying to engage enemy')
                left_click(window_list[0], x + int(w/2), y + int(h/2), 1.2)

            # Combat loop
            if in_combat is True:
                print("Attacking")
                for x_pos in range(attack_pos[0], attack_pos[0]+12, 3):
                    left_click(window_list[0], x_pos, attack_pos[1], 0.1)
                    sleep(0.1)

            if need_to_click_continue is True:
                print('Clicking continue')
                left_click(window_list[0], x_continue, y_continue, 0.1)
