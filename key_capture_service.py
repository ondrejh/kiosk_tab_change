#!/usr/bin/python3

''' The service captures the input devices and searches for key stroke events.
If no event found for presetted time the service starts to send the keyboard
shorcut request to KeyPress server. Together wit KeyPress server can be used
to change the browsers tabs in web kiosk, when input devices are idle.

author: Ondrej Hejda
date created: 16.4.2022
'''

import evdev
import select
import threading
from time import sleep
import click

from key_press_server import send_ctrl_tab, HOST, PORT


TIMEOUT = 30
STEP = 5

c = threading.Condition()
devs = [evdev.InputDevice(path) for path in evdev.list_devices()]
cnt = TIMEOUT
some_event = False


class DevThread(threading.Thread):

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.dev = device
        self.stopped = False

    def run(self):
        print('Start capture "{}"'.format(self.dev.name))
        while not self.stopped:
            r, w, x = select.select([self.dev], [], [])
            for event in self.dev.read():
                if event.type == evdev.ecodes.EV_KEY:
                    print(evdev.categorize(event))
                    c.acquire()
                    global some_event
                    some_event = True
                    c.release()
        print('Capturing "{}" stopped'.format(self.dev.name))

    def stop(self):
        self.stopped = True


def list_input_devices():

    return [evdev.InputDevice(path) for path in evdev.list_devices()]


def select_by_pattern(devices, list_of_patterns=[]):

    devs = []

    if len(list_of_patterns) > 0:
        for dev in devices:
            for pat in list_of_patterns:
                patlow = pat.lower()
                if dev.name.lower().find(patlow) > 0:
                    devs.append(dev)
                    break
    else:
        devs = devices

    return devs


@click.command()
@click.option('--list_devices', '-l', is_flag=True, default=False, help='List input devices.')
@click.option('--select', '-s', default=None, multiple=True, help='Select by content.')
@click.option('--timeout', '-t', default=TIMEOUT, type=int, help='Timeout to start generating keys.')
@click.option('--pause', '-p', default=STEP, type=int, help='Pause between key presses.')
@click.option('--host', default=HOST, help='KeyPress server ip address')
@click.option('--port', default=PORT, help='KeyPress server port')

def click_app(list_devices, select, timeout, pause, host, port):
    global cnt
    global some_event

    all_devs = list_input_devices()
    devs = select_by_pattern(all_devs, select)

    if list_devices:
        for dev in all_devs:
            print('SEL' if dev in devs else 'ign', dev.path, dev.name, dev.phys)
        return

    cnt = 0

    dev_threads = []
    for dev in devs:
        t = DevThread(dev)
        t.start()
        dev_threads.append(t)

    try:
        while True:
            c.acquire()
            some_event = False
            c.release()
            sleep(pause * 1.0)
            c.acquire()
            if some_event:
                cnt = timeout
                print('Countdown {}'.format(cnt))
            else:
                if cnt <= pause:
                    if cnt:
                        print('Start simulate CTRL + TAB')
                    cnt = 0
                    # keyboard shortcut CTRL + TAB
                    send_ctrl_tab(host, port)
                else:
                    cnt -= pause
                    print('Countdown {}'.format(cnt))
            c.release()
    except KeyboardInterrupt:
        pass

    for t in dev_threads:
        t.stop()
        #t.join()


if __name__ == "__main__":

    click_app()
