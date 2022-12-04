import os


# MONGODB_URL = os.getenv('DATABASE_URL')

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class Settings(BaseSettings):
    mongodb_url: str

    class Config:
        env_file = ".env"

        # env_prefix = 'FL_BACKEND_'
        fields = {
            'mongodb_url': {
                'env': 'FL_BACKEND_DATABASE_URL',
            },
        }

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            # here we choose to ignore arguments from init_settings
            return env_settings, file_secret_settings


def get_settings():
    return Settings()
