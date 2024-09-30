import configparser

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Loads the configuration file."""
        self.config.read(self.config_file)

    def get_app_config(self):
        """Fetches the app config settings."""
        app_config = {
            'screenshot_interval': int(self.config.get('App', 'screenshot_interval', fallback='300')),
            'screenshot_dir': self.config.get('App', 'screenshot_dir', fallback='./screenshots'),
            'capture_screenshots': self.config.get('App', 'capture_screenshots', fallback='true').lower() == 'true',
            'blur_screenshots': self.config.get('App', 'blur_screenshots', fallback='false').lower() == 'true',
            'mouse_movement_threshold': self.config.get('App', 'mouse_movement_threshold', fallback='1000'),
            'keyboard_input_threshold': self.config.get('App', 'keyboard_input_threshold', fallback='0.1')
        }
        return app_config

    def get_s3_config(self):
        """Fetches the S3 config settings."""
        s3_config = {
            'bucket_name': self.config.get('S3', 'bucket_name', fallback=''),
            'aws_access_key': self.config.get('S3', 'aws_access_key', fallback=''),
            'aws_secret_key': self.config.get('S3', 'aws_secret_key', fallback=''),
            'region': self.config.get('S3', 'region', fallback='us-east-1')
        }
        return s3_config

    def reload_config(self):
        """Reload the configuration file."""
        self.load_config()
