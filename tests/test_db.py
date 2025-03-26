from dataclasses import asdict

from sqlalchemy import select

from zero.models import Todo, User


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
            'todos': [],
        }


def test_create_todo(session, user, mock_db_time):
    with mock_db_time(model=Todo) as time:
        new_todo = Todo(
            title='Test Todo',
            description='Test Description',
            state='draft',
            user_id=user.id,
        )

        session.add(new_todo)
        session.commit()

        todo = session.scalar(select(Todo))

        assert asdict(todo) == {
            'id': 1,
            'title': 'Test Todo',
            'description': 'Test Description',
            'state': 'draft',
            'user_id': user.id,
            'updated_at': time,
            'created_at': time,
        }


def test_user_todo_relationship(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(user)

    user = session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]
