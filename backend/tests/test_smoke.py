from unittest.mock import AsyncMock

import pytest
from base.db_age import Database
from base.email import SendgridEmailer
from base.models import SendEmailQuery, AccountA14N
from fastapi.testclient import TestClient


def test_api_healthz(client):
    response = client.get('/api/v1/healthz')
    assert response.status_code == 200, 'Response code not 200'
    assert response.json() == {'status': True}


@pytest.mark.asyncio
async def test_api_send_email(
    client, mock_db: Database, mock_emailer: SendgridEmailer
):
    email_query = SendEmailQuery(email='pass-test-even-with-invalid-email.com')

    response = client.post('/api/v1/auth/send-email', json=email_query.dict())

    assert response.status_code == 200, 'Response code not 200'
    assert response.json() == {'status': 'ok'}
    mock_db.query_account_by_a14n_provider_type_and_value.assert_awaited_once()
    mock_db.add_account_new_a14n_signature.assert_awaited_once()
    mock_emailer.send_email.assert_awaited_once()


@pytest.mark.asyncio
async def test_api_confirm_email(client: TestClient, mock_db: Database):
    mock_db.query_account_by_a14n_signature_type_and_value = AsyncMock(
        return_value=AccountA14N(
            account_id='aaa',
            account_a14n_provider_id='bbb',
            account_a14n_signature_id='ccc',
        )
    )

    response = client.get('/api/v1/auth/confirm-email-with-aaaa')

    assert response.status_code == 200, 'Response code not 200'
    assert response.json() == {'status': 'ok'}
    assert response.cookies['auth'], 'No `auth` cookie set'
    mock_db.query_account_by_a14n_signature_type_and_value.assert_awaited_once()
