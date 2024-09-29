import configparser

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_s3_config(self):
        return {
            'bucket_name': self.config['S3']['bucket_name'],
            'aws_access_key': self.config['S3']['aws_access_key'],
            'aws_secret_key': self.config['S3']['aws_secret_key'],
            'region': self.config['S3']['region']
        }

    def get_app_config(self):
        return {
            'screenshot_interval': int(self.config['App']['screenshot_interval']),
            'screenshot_dir': self.config['App']['screenshot_dir']
        }
