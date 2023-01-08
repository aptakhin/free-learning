from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings."""

    db_url: str
    self_url: str

    sender_email: str
    sendgrid_token: str

    jwt_a14n_token: str

    class Config(object):
        env_file = '.env'

        fields = {
            'db_url': {
                'env': 'FL_BACKEND_DATABASE_URL',
            },
            'self_url': {
                'env': 'FL_BACKEND_SELF_URL',
            },
            'sender_email': {
                'env': 'FL_SENDER_EMAIL',
            },
            'sendgrid_token': {
                'env': 'FL_SENDGRID_TOKEN',
            },
            'jwt_a14n_token': {
                'env': 'FL_JWT_A14N_TOKEN',
            },
        }


def get_settings():  # noqa: D103
    return Settings()


FL_MODULE_BASE = 'com.freelearning.base'
FL_MODULE_WORKDOMAIN = 'com.freelearning.workdomain'

FL_MODULE_BASE_ENTITY = 'com.freelearning.base.entity'
FL_MODULE_BASE_TAG = 'com.freelearning.base.tag'
FL_MODULE_BASE_WEB_ROUTE = 'com.freelearning.base.web_route'
FL_MODULE_BASE_GROUP_ALIAS = 'com.freelearning.base.group_alias'
FL_MODULE_BASE_LINK_CHILD_OF = 'com.freelearning.base.CHILD_OF'
FL_MODULE_BASE_LINK_NEXT_OF = 'com.freelearning.base.NEXT_OF'

FL_ANONYMOUS_ACCOUNT_ID = '4a603ae1-513c-4aee-9d94-a18f7f09e5e3'
