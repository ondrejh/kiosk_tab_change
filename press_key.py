#!/usr/bin/python3

''' The simple script simulation CTRL + TAB press '''

from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()


sleep(2)

keyboard.press(Key.ctrl.value)
keyboard.press(Key.tab.value)
keyboard.release(Key.tab.value)
keyboard.release(Key.ctrl.value)

sleep(1)
