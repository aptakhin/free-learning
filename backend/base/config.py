from pydantic import BaseSettings
# from pydantic.env_settings import SettingsSourceCallable


class Settings(BaseSettings):
    """Settings."""
    db_url: str
    self_url: str

    class Config:
        env_file = '.env'

        # env_prefix = 'FL_BACKEND_'
        fields = {
            'db_url': {
                'env': 'FL_BACKEND_DATABASE_URL',
            },
            'self_url': {
                'env': 'FL_BACKEND_SELF_URL',
            },
        }


def get_settings():
    return Settings()


FL_MODULE_BASE = 'base.freelearning.org'
FL_MODULE_WORKDOMAIN = 'workdomain.freelearning.org'
