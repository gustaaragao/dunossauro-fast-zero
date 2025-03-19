from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from zero.app import app
from zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # Cria uma Engine em Memória para o banco
    engine = create_engine('sqlite:///:memory:')

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

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
