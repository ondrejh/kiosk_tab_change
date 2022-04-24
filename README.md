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

## Instalation

1) Download the script and enter its folder.
```
git clone https://github.com/ondrejh/kiosk_tab_change
cd kiosk_tab_change
```

2) Install python libraries (for root too)
```
sudo pip3 install evdev
sudo pip3 install click
```

3) Test the key capture script
```
sudo ./key_capture_service.py -l
sudo ./key_capture_service.py
```
After a while the script should say: `Can't connect to KeyPress server at localhost:9999!`. Thats right, as long as the key press server is not started.

4) Change the script target in the service file if needed.

5) Install the key capture service.
```
sudo cp key_capture.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable key_capture.service
```

6) Run key press server at user startup.
```
echo "/home/kiosek/kiosk_tab_change/key_press_server.py &" >> ~/.config/lxsession/LXDE/autostart
```

7) Restart the user session.

ToDo: Test and update the installation...
