import time
import schedule
import pytz
from tzlocal import get_localzone
from datetime import datetime
from screenshot_capture import ScreenshotCapture
from s3_uploader import S3Uploader
from config_manager import ConfigManager
from activity_tracker import ActivityTracker

# Time zone tracking variable
current_timezone = None

# Function to detect the system's time zone using tzlocal
def get_current_timezone():
    return str(get_localzone())  # Returns IANA-compliant time zone, e.g., 'Asia/Kolkata'

# Function to get current timestamp with timezone
def get_current_timestamp():
    tz = pytz.timezone(current_timezone)
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')

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
    blur_screenshots = new_app_config['blur_screenshots']
    capture_screenshots = new_app_config['capture_screenshots']
    screenshot_interval = new_app_config['screenshot_interval']

    # Update screenshot capture settings dynamically
    screenshot_capture.blur_screenshots = blur_screenshots

    print(f"Configuration reloaded: {new_app_config}")
    return new_app_config

# Get initial settings
blur_screenshots = app_config['blur_screenshots']
capture_screenshots = app_config['capture_screenshots']
screenshot_interval = app_config['screenshot_interval']

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
            print(f"Screenshot captured at {get_current_timestamp()}")  # Log with adjusted timestamp
        else:
            print(f"User is idle. No screenshot taken at {get_current_timestamp()}.")
    else:
        print("Screenshot capture disabled in configuration.")

# Function to update the scheduled screenshot job
def update_screenshot_job():
    schedule.clear()  # Clear all scheduled jobs
    schedule.every(screenshot_interval).seconds.do(capture_and_upload)
    print(f"Screenshot interval updated to {screenshot_interval} seconds.")

# Detect time zone changes
def detect_timezone_change():
    global current_timezone
    new_timezone = get_current_timezone()
    if current_timezone != new_timezone:
        current_timezone = new_timezone
        print(f"Time zone changed to {current_timezone}")
        # Adjust any time-based activities if necessary, such as updating logs or schedules

# Scheduling screenshots to be captured at the given interval
update_screenshot_job()

# Periodically reload configuration every 60 seconds
schedule.every(60).seconds.do(reload_configuration).tag('config_reload')

# Periodically check for time zone changes every 30 seconds
schedule.every(30).seconds.do(detect_timezone_change).tag('timezone_check')

# Start activity tracking and scheduling
activity_tracker.start_tracking()

# Set initial time zone
current_timezone = get_current_timezone()
print(f"Initial time zone is {current_timezone}")

# Main loop for the app
while True:
    schedule.run_pending()
    time.sleep(1)
    # Check if the interval has changed, and reschedule screenshots if needed
    new_config = reload_configuration()
    if screenshot_interval != new_config['screenshot_interval']:
        screenshot_interval = new_config['screenshot_interval']
        update_screenshot_job()
