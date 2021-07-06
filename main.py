import sys
import time
from pynput import keyboard
from multiprocessing import Process, Event, Queue

import controller

key_toggle_bot = '<f1>'
key_mouse_pos = '<f2>'
key_command = '<f3>'
key_get_hwnd = '<insert>'
key_exit = '<end>'


def hotkey_thr(command_queue, thread_event):

    def com_toggle_bot():
        if thread_event.is_set():
            thread_event.clear()
            print('Pausing')
        else:
            thread_event.set()
            print('Playing')

    def com_mouse_pos():
        command = 'mouse pos'
        command_queue.put(command)

    def com_command():    
        command = 'command'
        command_queue.put(command)
    
    def com_get_hwnd():
        command = 'get hwnd'
        command_queue.put(command)

    def com_exit():
        command = 'exit'
        command_queue.put(command)
        sys.exit(0)

    with keyboard.GlobalHotKeys({
        key_toggle_bot: com_toggle_bot,
        key_mouse_pos: com_mouse_pos,
        key_command: com_command,
        key_get_hwnd: com_get_hwnd,
        key_exit: com_exit
    }) as h:
        h.join()


if __name__ == '__main__':

    command_queue = Queue()
    thread_event = Event()

    hotkey_thread = Process(target=hotkey_thr, args=(
                            command_queue, thread_event))

    bot_thread = Process(target=controller.bot_thread, args=(
        command_queue, thread_event))

    hotkey_thread.start()
    bot_thread.start()
