import time
from pynput import mouse, keyboard

class ActivityTracker:
    def __init__(self, idle_time_limit=300, mouse_movement_threshold=1000, keyboard_input_threshold=0.1):
        self.idle_time_limit = idle_time_limit
        self.mouse_movement_threshold = mouse_movement_threshold
        self.keyboard_input_threshold = keyboard_input_threshold
        self.last_activity_time = time.time()

        # Mouse and keyboard listeners
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)

    def start_tracking(self):
        print("Tracking user activity...")
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def on_move(self, x, y):
        """Callback for mouse movement events."""
        self.last_activity_time = time.time()

    def on_key_press(self, key):
        """Callback for keyboard press events."""
        self.last_activity_time = time.time()

    def get_idle_time(self):
        """Returns the time in seconds since the last user activity."""
        return time.time() - self.last_activity_time
