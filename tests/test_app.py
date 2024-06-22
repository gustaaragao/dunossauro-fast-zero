from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo():
    # 'AAA' -> fases de um teste

    client = TestClient(app)  # Arrange (organização)

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmar)
    assert response.json() == {'message': 'Olá mundo!!'}  # Assert


def test_read_html_deve_retornar_ola_mundo():
    client = TestClient(app)  # Arrange (organização)

    response = client.get('/html')  # Act (ação)

    assert response.text == '<html><h1>Olá mundo!!</h1></html>'  # Assert
