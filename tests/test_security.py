from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from fast_zero.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_jwt():
    data_payload = {'sub': 'test@test.com'}

    token = create_access_token(data_payload)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data_payload['sub']
    assert result['exp']  # Testa se o valor de exp foi adicionado ao token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_without_username(session):
    none_payload = {'sub': None}

    none_token = create_access_token(none_payload)

    with pytest.raises(HTTPException) as exception_info:
        get_current_user(session, none_token)

    assert exception_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception_info.value.detail == 'Could not validate credentials'


def test_get_current_user_not_found_in_db(session):
    wrong_payload = {'sub': 'wrong@email.com'}

    wrong_token = create_access_token(wrong_payload)

    with pytest.raises(HTTPException) as exception_info:
        get_current_user(session, wrong_token)

    assert exception_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception_info.value.detail == 'Could not validate credentials'
