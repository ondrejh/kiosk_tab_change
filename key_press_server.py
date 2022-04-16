#!/usr/bin/python3

''' KeyPress server application:
Binds on HOST / PORT (can be changed with cmd options) and listens request to
send the keyboard shortcut on the local machine. The current version only
supports CTRL + TAB. The program also contents the example client function.

author: Ondrej Hejda
date created: 16.4.2022
'''

import click


HOST = 'localhost'
PORT = 9999


def send_ctrl_tab(host=HOST, port=PORT):

    ''' KeyPress server example client function. Calling the function sends
    request to server. Server should react by simulation CTRL + TAB press.'''

    import socket

    data = b'CTRL + TAB'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(data)
        print("Request {} sent".format(data.decode('ascii')))
    except ConnectionRefusedError:
        print("Can't connect to KeyPress server at {}:{}!".format(host, port))


@click.command()
@click.option('--host', '-h', default=HOST, help='KeyPress server host ip address.')
@click.option('--port', '-p', default=PORT, type=int, help='KeyPress server port.')

def clickApp(host, port):

    from pynput.keyboard import Controller, Key
    import socketserver

    keyboard = Controller()

    class TCPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            self.data = self.request.recv(1024).strip()
            print("{} sent: {}".format(self.client_address[0], self.data.decode('ascii')))
            if self.data == b'CTRL + TAB':
                keyboard.press(Key.ctrl.value)
                keyboard.press(Key.tab.value)
                keyboard.release(Key.tab.value)
                keyboard.release(Key.ctrl.value)

    print('KeyPress server started at {}:{}.'.format(host, port))

    with socketserver.TCPServer((host, port), TCPHandler) as server:
        server.serve_forever()


if __name__ == "__main__":

    clickApp()
