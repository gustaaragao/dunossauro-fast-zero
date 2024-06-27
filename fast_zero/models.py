from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()  # Registra "metadados" da Tabela (DB)

"""
Mapeia para uma "dataclass"
dataclass -> Estrutura do Python que é uma Classe com *APENAS* atributos(dados)
"""


@table_registry.mapped_as_dataclass
class User:
    # __tablename__ -> Nome da Tabela
    __tablename__ = 'users'

    # Mapped -> o SQLAlchemy vai se "virar" para mapeiar isso para o SQL
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),  # O 'now' é do Servidor
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now()
    )
