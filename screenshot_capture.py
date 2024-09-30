from PIL import Image, ImageFilter
import pyautogui
import os
import time

class ScreenshotCapture:
    def __init__(self, screenshot_dir, blur_screenshots=False):
        self.screenshot_dir = screenshot_dir
        self.blur_screenshots = blur_screenshots

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

    def capture_screenshot(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")
        
        # Capture the screenshot
        screenshot = pyautogui.screenshot()

        # Blur the screenshot if the setting is enabled
        if self.blur_screenshots:
            screenshot = screenshot.filter(ImageFilter.GaussianBlur(15))

        screenshot.save(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        return screenshot_path
