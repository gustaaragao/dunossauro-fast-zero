import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from zero.app import app
from zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # Cria a Engine em Memória para o banco para criar a Sessão
    engine = create_engine('sqlite:///:memory:')

    # Cria todas tabelas registradas no registry
    table_registry.metadata.create_all(engine)

    # Cria uma Session para os testes usarem
    with Session(engine) as session:
        # Injeta uma instância de Session
        yield session

    table_registry.metadata.drop_all(engine)
    # Após cada teste todas as tabelas do banco são eliminadas
    # -> Garante independência entre os testes
