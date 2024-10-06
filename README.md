WorkStatus.io - Employee Activity Tracker

Overview
This project is a Python-based desktop agent that tracks employee activity by capturing screenshots, detecting user input (keyboard and mouse), and uploading the data securely to Amazon S3. The project includes configurable features such as time intervals for screenshot capture, time zone management, and the option to blur screenshots.

Features
- Screenshot capture at configurable intervals
- Activity tracking for keyboard and mouse input
- Secure data upload to Amazon S3
- Real-time configuration updates
- Time zone management for accurate timestamps
- Anti-scripted activity detection to avoid false positives

Libraries Used

1. boto3
- Purpose: Interacting with Amazon Web Services (AWS), specifically for uploading files (screenshots and logs) to an S3 bucket.
- Usage in project: 
  - Uploads screenshots to Amazon S3 using secure credentials and handles large files efficiently through chunked uploads.

pip install boto3

2. Pillow (PIL)
Purpose: Image manipulation and processing.
Usage in project:
Capturing screenshots.
Optionally applying a blur effect to images before uploading them.

pip install pillow

3. pynput
Purpose: Monitoring keyboard and mouse events.
Usage in project:
Tracks user activity by detecting keyboard and mouse inputs.
Differentiates genuine user input from script-based activity by analyzing input patterns.

pip install pynput

4. schedule
Purpose: Simple, human-friendly job scheduling for Python.
Usage in project:
Schedules tasks like taking screenshots and uploading them at user-configured intervals.

pip install schedule

5. configparser
Purpose: Reading and writing configuration files (config.ini).
Usage in project:
Manages and reads application configurations such as screenshot intervals, S3 credentials, and activity thresholds.

pip install configparser

6. pytz
Purpose: Handling time zones and ensuring accurate timestamps across different time zones.
Usage in project:
Adjusts and manages timestamps based on the user's local time zone.

pip install pytz

7. psutil
Purpose: System and process utilities.
Usage in project:
Tracks system-level events like idle time, which helps in identifying whether the user is active or not.

pip install psutil

8. zlib
Purpose: Compression utility (part of Python’s standard library).
Usage in project:
Compresses screenshot files before uploading to reduce upload time and storage space.

9. logging
Purpose: Standard Python library for logging information.
Usage in project:
Logs events, activities, and errors such as screenshot captures and failed uploads to a file specified in the configuration.

Configuration
The configuration for the project is stored in a config.ini file, which allows you to customize settings like:

Screenshot interval
Whether to blur screenshots
S3 bucket credentials and region
Activity thresholds for mouse and keyboard inputs

Usage

1. Modify the config.ini file with your S3 credentials and other application settings.
2. Run the application:
   python main.py
