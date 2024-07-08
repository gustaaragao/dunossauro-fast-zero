from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    # Verifica o HTTP Status Code
    assert response.status_code == HTTPStatus.OK
    # Verifica o tipo do Token (Bearer)
    assert token['token_type'] == 'Bearer'
    # Verifica se o token de acesso foi criado
    assert 'access_token' in token


def test_get_token_with_wrong_email(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong_email', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_with_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
