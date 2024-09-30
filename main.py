import time
import schedule
from screenshot_capture import ScreenshotCapture
from s3_uploader import S3Uploader
from config_manager import ConfigManager
from activity_tracker import ActivityTracker

# Initialize configuration and components
config_manager = ConfigManager()
app_config = config_manager.get_app_config()
s3_config = config_manager.get_s3_config()

# Get screenshot capture settings, with default values
blur_screenshots = app_config.get('blur_screenshots', 'false').lower() == 'true'
capture_screenshots = app_config.get('capture_screenshots', 'true').lower() == 'true'

# Initialize screenshot capture and uploader
screenshot_capture = ScreenshotCapture(
    app_config['screenshot_dir'], 
    blur_screenshots=blur_screenshots
)

uploader = S3Uploader(
    s3_config['bucket_name'], 
    s3_config['aws_access_key'], 
    s3_config['aws_secret_key'], 
    s3_config['region']
)

# Get activity tracking thresholds, with default values
mouse_movement_threshold = int(app_config.get('mouse_movement_threshold', 1000))
keyboard_input_threshold = float(app_config.get('keyboard_input_threshold', 0.1))

activity_tracker = ActivityTracker(
    idle_time_limit=app_config['screenshot_interval'],
    mouse_movement_threshold=mouse_movement_threshold,
    keyboard_input_threshold=keyboard_input_threshold
)

# Function to capture and upload screenshots
def capture_and_upload():
    if capture_screenshots:
        if activity_tracker.get_idle_time() < app_config['screenshot_interval']:
            screenshot_path = screenshot_capture.capture_screenshot()
            uploader.upload_file(screenshot_path, f"screenshots/{screenshot_path.split('/')[-1]}")
        else:
            print("User is idle. No screenshot taken.")
    else:
        print("Screenshot capture disabled in configuration.")

# Scheduling screenshots to be captured every X seconds
schedule.every(app_config['screenshot_interval']).seconds.do(capture_and_upload)

# Start activity tracking and scheduling
activity_tracker.start_tracking()

# Main loop for the app
while True:
    schedule.run_pending()
    time.sleep(1)
