from http import HTTPStatus

from jwt import decode

from zero.security import SECRET_KEY, create_access_token


def test_jwt():
    # Dados que serão assinados pelo Token JWT
    data = {'test': 'test'}

    # Criação do Token
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
