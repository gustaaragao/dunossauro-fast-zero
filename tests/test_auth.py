from http import HTTPStatus


def test_login_for_access_token(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_login_for_access_token_with_email_not_registered(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': 'not_registered@email.com',
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_for_access_token_with_incorrect_password(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': user.email,
            'password': 'wrong_secret',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
