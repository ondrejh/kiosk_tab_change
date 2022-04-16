# Web Kiosk Tab Change script

The script capturing the input devices and sending CTRL + TAB when idle.

It consists of two programs.

The first is **key_capture_service.py** which should capture
the input devices for keystroke events and sends keyboard shortcut requests
when there are no events present for presetted time. The capture service should
run with root privileges.

The second application is KeyPress server **key_press_server.py**. It should
run with X server user rights. The server listens for keyboard shortcut request
and simulated the keyboard shortcut pressing every time the request received.

ToDo: Document the script installation.
