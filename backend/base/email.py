from abc import ABC, abstractmethod
import httpx
import logging

from base.config import Settings, get_settings
from base.exceptions import CantSendEmail
from fastapi import Depends


logger = logging.getLogger(__name__)


class Emailer(ABC):
    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def send_email(
        self, *, to: str, subject: str, content: list[dict[str, str]]
    ):
        ...


class SendgridEmailer(Emailer):
    def __init__(self, token: str, from_: str) -> None:
        self._from = from_
        headers = {
            'Authorization': f'Bearer {token}',
        }
        self._client = httpx.AsyncClient(
            base_url='https://api.sendgrid.com',
            headers=headers,
        )

    async def close(self):
        await self._client.aclose()

    async def send_email(
        self, *, to: str, subject: str, content: list[dict[str, str]]
    ):
        json_body = {
            'personalizations': [{'to': [{'email': to}]}],
            'from': {'email': self._from},
            'subject': subject,
            'content': content,
        }
        response = await self._client.post(
            '/v3/mail/send',
            json=json_body,
        )
        if response.status_code != 202:
            logger.error(
                'Got response code=%s with response=%s',
                response.status_code,
                response.text,
            )
            raise CantSendEmail(response.text)


async def get_emailer(
    settings: Settings = Depends(get_settings),
) -> Emailer:  # noqa: B008
    emailer = SendgridEmailer(
        token=settings.sendgrid_token,
        from_=settings.sender_email,
    )

    yield emailer

    await emailer.close()
