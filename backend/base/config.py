from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings."""

    db_url: str
    self_url: str

    class Config(object):
        env_file = '.env'

        fields = {
            'db_url': {
                'env': 'FL_BACKEND_DATABASE_URL',
            },
            'self_url': {
                'env': 'FL_BACKEND_SELF_URL',
            },
        }


def get_settings():  # noqa: D103
    return Settings()


FL_MODULE_BASE = 'com.freelearning.base'
FL_MODULE_WORKDOMAIN = 'com.freelearning.workdomain'

FL_MODULE_BASE_ENTITY = 'com.freelearning.base.entity'
FL_MODULE_BASE_TAG = 'com.freelearning.base.tag'
FL_MODULE_BASE_ALIAS = 'com.freelearning.base.alias'
FL_MODULE_BASE_LINK_CHILD_OF = 'com.freelearning.base.CHILD_OF'
