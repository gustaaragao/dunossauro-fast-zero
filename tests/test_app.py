from http import HTTPStatus


def test_root(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_html(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo! </h1>' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'gustavo',
            'email': 'gustavo@email.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'gustavo',
        'email': 'gustavo@email.com',
    }


def test_get_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'gustavo', 'email': 'gustavo@email.com'}
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'henrique',
            'email': 'henrique@email.com',
            'password': 'new_secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'henrique',
        'email': 'henrique@email.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/-1',
        json={
            'username': 'henrique',
            'email': 'henrique@email.com',
            'password': 'new_secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
