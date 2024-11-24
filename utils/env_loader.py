import os
from dotenv import load_dotenv

class EnvLoader:
    def __init__(self, env_path='.env'):
        self.env_path = env_path
        self.load_env()

    def load_env(self):
        if os.path.exists(self.env_path):
            load_dotenv(self.env_path)
        else:
            raise FileNotFoundError(f"Environment file not found: {self.env_path}")

    def get_env(self, key):
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Environment variable {key} is not set in {self.env_path}")
        return value