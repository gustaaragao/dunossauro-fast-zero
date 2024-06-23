from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'name',
            'email': 'email@test.com',
            'password': 'password',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'id': 1,
        'username': 'name',
        'email': 'email@test.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    """
    Observacao:
    Isso é uma péssima prática, pois esse teste depende do anterior...
    Porém, como não temos um DB é o melhor que podemos fazer
    """
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'name',
                'email': 'email@test.com',
            },
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'name',
        'email': 'email@test.com',
    }


def test_read_user_not_found(client):
    response = client.get('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'name2',
            'email': 'email2@test.com',
            'password': 'password2',
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'name2',
        'email': 'email2@test.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'name2',
            'email': 'email2@test.com',
            'password': 'password2',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}
