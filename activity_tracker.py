from pynput import mouse, keyboard
import time

class ActivityTracker:
    def __init__(self):
        self.last_activity = time.time()

    def on_move(self, x, y):
        self.last_activity = time.time()

    def on_click(self, x, y, button, pressed):
        self.last_activity = time.time()

    def on_key_press(self, key):
        self.last_activity = time.time()

    def get_idle_time(self):
        return time.time() - self.last_activity

    def start_tracking(self):
        # Start tracking mouse and keyboard
        mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        mouse_listener.start()
        keyboard_listener.start()
