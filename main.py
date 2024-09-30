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

# Function to update the current configuration dynamically
def reload_configuration():
    config_manager.reload_config()
    new_app_config = config_manager.get_app_config()

    global blur_screenshots, capture_screenshots, screenshot_interval, screenshot_capture
    # Apply new settings if they've changed
    blur_screenshots = new_app_config['blur_screenshots']  # No need for .lower() since it's already a boolean
    capture_screenshots = new_app_config['capture_screenshots']  # Already boolean
    screenshot_interval = new_app_config['screenshot_interval']  # Already an integer

    # Update screenshot capture settings dynamically
    screenshot_capture.blur_screenshots = blur_screenshots

    print(f"Configuration reloaded: {new_app_config}")
    return new_app_config

# Get initial settings
blur_screenshots = app_config['blur_screenshots']  # Already boolean
capture_screenshots = app_config['capture_screenshots']  # Already boolean
screenshot_interval = app_config['screenshot_interval']  # Already integer

# Initialize screenshot capture and uploader
screenshot_capture = ScreenshotCapture(app_config['screenshot_dir'], blur_screenshots=blur_screenshots)
uploader = S3Uploader(s3_config['bucket_name'], s3_config['aws_access_key'], s3_config['aws_secret_key'], s3_config['region'])

# Initialize activity tracker
activity_tracker = ActivityTracker(
    idle_time_limit=screenshot_interval,
    mouse_movement_threshold=int(app_config['mouse_movement_threshold']),
    keyboard_input_threshold=float(app_config['keyboard_input_threshold'])
)

# Function to capture and upload screenshots
def capture_and_upload():
    if capture_screenshots:
        if activity_tracker.get_idle_time() < screenshot_interval:
            screenshot_path = screenshot_capture.capture_screenshot()
            uploader.upload_file(screenshot_path, f"screenshots/{screenshot_path.split('/')[-1]}")
        else:
            print("User is idle. No screenshot taken.")
    else:
        print("Screenshot capture disabled in configuration.")

# Function to update the scheduled screenshot job
def update_screenshot_job():
    schedule.clear()  # Clear all scheduled jobs
    schedule.every(screenshot_interval).seconds.do(capture_and_upload)
    print(f"Screenshot interval updated to {screenshot_interval} seconds.")

# Scheduling screenshots to be captured at the given interval
update_screenshot_job()

# Periodically reload configuration every 60 seconds
schedule.every(60).seconds.do(reload_configuration).tag('config_reload')

# Start activity tracking and scheduling
activity_tracker.start_tracking()

# Main loop for the app
while True:
    schedule.run_pending()
    time.sleep(1)
    # Check if the interval has changed, and reschedule screenshots if needed
    new_config = reload_configuration()
    if screenshot_interval != new_config['screenshot_interval']:
        screenshot_interval = new_config['screenshot_interval']
        update_screenshot_job()
