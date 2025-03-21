from http import HTTPStatus


def test_create_todo(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'Test Description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test Description',
        'state': 'draft',
    }

def test_read_todos(client, token):
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    