from dataclasses import asdict

from sqlalchemy import select

from zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='Gustavo', email='gustavo@email.com', password='secret'
        )

        # O usuário está na Sessão, mas não no Banco (ESTADO TRANSIENTE)
        # --> Padrão: Unidade de Trabalho
        session.add(new_user)
        # Performar as ações no Banco
        session.commit()

        user = session.scalar(select(User).where(User.username == 'Gustavo'))

        assert asdict(user) == {
            'id': 1,
            'username': 'Gustavo',
            'email': 'gustavo@email.com',
            'password': 'secret',
            'updated_at': time,
            'created_at': time,
        }
