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

screenshot_capture = ScreenshotCapture(app_config['screenshot_dir'])
uploader = S3Uploader(s3_config['bucket_name'], s3_config['aws_access_key'], s3_config['aws_secret_key'], s3_config['region'])
activity_tracker = ActivityTracker()

# Function to capture and upload screenshots
def capture_and_upload():
    if activity_tracker.get_idle_time() < app_config['screenshot_interval']:
        screenshot_path = screenshot_capture.capture_screenshot()
        uploader.upload_file(screenshot_path, f"screenshots/{screenshot_path.split('/')[-1]}")

# Scheduling screenshots to be captured every X seconds
schedule.every(app_config['screenshot_interval']).seconds.do(capture_and_upload)

# Start activity tracking and scheduling
activity_tracker.start_tracking()

# Main loop for the app
while True:
    schedule.run_pending()
    time.sleep(1)
