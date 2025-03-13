from sqlalchemy import select

from zero.models import User


def test_create_user(session):
    new_user = User(
        username='Gustavo', email='gustavo@email.com', password='secret'
    )

    # O usuário está na Sessão, mas não no Banco (ESTADO TRANSIENTE)
    # --> Padrão: Unidade de Trabalho
    session.add(new_user)
    # Performar as ações no Banco
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Gustavo'))
    # .scalar() -> Pega o primeiro resultado da Query e converte para um objeto
    # select, where -> São equivalentes aos comandos do SQL

    assert user.username == 'Gustavo'
