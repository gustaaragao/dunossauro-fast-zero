from contextlib import contextmanager
from datetime import datetime

import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from zero.app import app
from zero.database import get_session
from zero.models import User, table_registry
from zero.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        # Adiciona no lugar a fixture de session
        app.dependency_overrides[get_session] = get_session_override
        yield client

    # Limpa a sobrescrita que fizemos no app para usar a fixture de session.
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # Cria uma Engine em Memória para o banco
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # Cria todas tabelas registradas no registry
    table_registry.metadata.create_all(engine)

    # Cria uma Session para os testes usarem
    with Session(engine) as session:
        # Injeta uma instância de Session
        yield session

    # Após cada teste todas as tabelas do banco são eliminadas
    # -> Garante independência entre os testes
    table_registry.metadata.drop_all(engine)


@contextmanager  # Cria um gerenciador de contexto (with)
# * garante que todos os parâmetros sejam chamados de forma explícita
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    # hook(mapper, connection, target)
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    password = 'secret'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def other_user(session):
    password = 'secret'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User  # Retorne objs da classe User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
