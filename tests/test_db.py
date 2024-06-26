from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='gusta', password='secret', email='gusta@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'gusta'))

    assert user.username == 'gusta'
