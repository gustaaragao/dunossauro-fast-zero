import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture()
def session():
    # Conexão com o banco de dados (sqlite3)
    # :memory: -> cria DB em Memória
    engine = create_engine(
        'sqlite:///:memory:',
        # o DB e Aplicação estão em Threads diferentes.
        connect_args={'check_same_thread': False},
        # Não crie vários recursos, use sempre o mesmo.
        poolclass=StaticPool,
    )

    """
    table_registry conhece todas as tabelas (metadados)
    |-> criar todas as tabelas a partir da Engine
    """
    table_registry.metadata.create_all(engine)

    # with -> gerenciamento de contexto
    with Session(engine) as session:
        yield session  # Geradores/Corrotinas

    table_registry.metadata.drop_all(engine)  # Destruir o DB


@pytest.fixture()
def client(session):
    def get_session_override():
        return session  # Usa o DB 'sqlite:///:memory:'

    with TestClient(app) as client:
        # Sobrescrever uma nova sessão para testes
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def user(session):
    password = 'password'

    user = User(
        username='test',
        email='test@email.com',
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Monkey Patch -> alterar um objeto em tempo de execução
    user.clean_password = password

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
