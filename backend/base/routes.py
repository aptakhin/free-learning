"""."""

import logging
from typing import Optional
from http import HTTPStatus

from base.config import FL_MODULE_BASE, Settings, get_settings, FL_ANONYMOUS_ACCOUNT_ID
from base.db import get_db, Database
from base.email import get_emailer, Emailer
from base.models import Entity, EntityUpsertResult, Link, LinkUpsertResult, EntityQueryResult, EntityQuery, AccountAuthToken, SendEmailQuery, Account, AccountA14N
from base.view import prepare_view_inplace
import jwt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


auth_router = APIRouter(
    prefix='/api/v1',
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)


@auth_router.post('/auth/send-email')
async def send_email(
    send_email_query: SendEmailQuery,
    emailer: Emailer = Depends(get_emailer),  # noqa: B008, WPS404
    db: Database = Depends(get_db),  # noqa: B008, WPS404
):
    account: Optional[Account] = await db.query_account_by_a14n_provider_type_and_value(
        provider_type='email',
        provider_value=send_email_query.email,
    )

    account_id = account.account_id if account else FL_ANONYMOUS_ACCOUNT_ID

    activation_phrase = 'magic-words'
    await db.add_account_new_a14n_signature(
        account_id=account_id,
        signature_type='email',
        signature_value=activation_phrase,
    )

    link = 'http://localhost:8000/api/v1/auth/confirm-email-with-{}'.format(activation_phrase)

    await emailer.send_email(
        to=send_email_query.email,
        subject='Freelearning activation link',
        content=[{'type': 'text/plain', 'value': 'Enter here: {}'.format(link)}],
    )

    return {'status': 'ok'}


@auth_router.get('/auth/confirm-email-with-{activation_phrase:path}')
async def confirm_email(
    activation_phrase: str,
    request: Request,
    db: Database = Depends(get_db),  # noqa: B008, WPS404
    settings: Settings = Depends(get_settings),  # noqa: B008, WPS404
):
    account_a14n: Optional[AccountA14N] = await db.query_account_by_a14n_signature_type_and_value(signature_type='email', signature_value=activation_phrase)

    if not account_a14n:
        raise ValueError('ss')
        return JSONResponse(content={'status': 'not-ok'}, status_code=HTTPStatus.UNAUTHORIZED)

    if account_a14n.account_id == FL_ANONYMOUS_ACCOUNT_ID:
        # Register new account by confirmed provider
        async with db._engine.begin() as _:
            account = await db.add_new_account()
            await db.move_a14n_provider_to_account(
                account_a14n_provider_id=account_a14n.account_a14n_provider_id,
                account_id=account.account_id,
            )
            account_a14n.account_id = account.account_id

    account_auth_token = AccountAuthToken(
        account_id=account_a14n.account_id,
    )

    encoded_auth = jwt.encode(
        payload=account_auth_token.dict(),
        key=settings.jwt_a14n_token,
        algorithm='HS256',
    )

    request_headers = request.headers
    device = {
        header: request_headers[header]
        for header in ('user-agent', 'sec-ch-ua', 'sec-ch-ua-platform', 'sec-ch-ua-mobile')
        if header in request_headers
    }
    await db.confirm_a14n_with_device(
        account_a14n_signature_id=account_a14n.account_a14n_signature_id,
        device=device,
    )
    # >>> jwt.decode(encoded, "secret", algorithms=["HS256"])
    # {'some': 'payload'}

    response = JSONResponse(content={'status': 'ok'})
    response.set_cookie(key='auth', value=encoded_auth)
    return response


router = APIRouter(
    prefix='/{org_slug}/api/%s/v1' % (FL_MODULE_BASE,),
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/upsert-entity', response_model=EntityUpsertResult)
async def upsert_entity(
    entity: Entity,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> EntityUpsertResult:
    """Upserts entity."""
    result_row = await db.upsert_entity(entity)
    return EntityUpsertResult(
        id=result_row['id'],
    )


@router.post('/query-linked/', response_model=EntityQueryResult)
async def query_linked(
    query: EntityQuery,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> EntityQueryResult:
    """Query entity."""
    query_result = await db.query_linked(query)

    riched_result = []
    for it in query_result:
        riched_result.append([
            prepare_view_inplace(it[0]),
            it[1],
            prepare_view_inplace(it[2]),
        ])

    riched_result.sort(key=lambda it: it[0]['id'])

    return EntityQueryResult(
        query_result=riched_result,
    )


@router.post('/upsert-link', response_model=LinkUpsertResult)
async def upsert_link(
    link: Link,
    org_slug: str,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> LinkUpsertResult:
    """Upserts link."""
    result_row = await db.upsert_link(link)
    return LinkUpsertResult(
        id=result_row['id'],
    )
