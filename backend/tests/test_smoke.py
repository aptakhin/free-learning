"""."""


def test_api_healthz(client):
    response = client.get('/api/v1/healthz')
    assert response.status_code == 200
    assert response.json() == {'status': True}
