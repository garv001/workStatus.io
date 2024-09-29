import pyautogui
import time
import os

class ScreenshotCapture:
    def __init__(self, screenshot_dir):
        self.screenshot_dir = screenshot_dir
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

    def capture_screenshot(self):
        # Generate a timestamp-based file name
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filepath = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")
        
        # Capture screenshot and save it
        pyautogui.screenshot(filepath)
        print(f"Screenshot saved to {filepath}")
        return filepath
