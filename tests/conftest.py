import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    # Conexão com o banco de dados (sqlite3)
    # :memory: -> cria DB em Memória
    engine = create_engine('sqlite:///:memory:')

    """
    table_registry conhece todas as tabelas (metadados)
    |-> criar todas as tabelas a partir da Engine
    """
    table_registry.metadata.create_all(engine)

    # with -> gerenciamento de contexto
    with Session(engine) as session:
        yield session  # Geradores/Corrotinas

    table_registry.metadata.drop_all(engine)  # Destruir o DB
