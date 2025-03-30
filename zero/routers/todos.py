from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from zero.database import get_session
from zero.models import Todo, User
from zero.schemas import (
    FilterTodo,
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic, status_code=HTTPStatus.CREATED)
def create_todo(todo: TodoSchema, user: CurrentUser, session: DBSession):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def read_todos(
    user: CurrentUser,
    session: DBSession,
    filters: Annotated[FilterTodo, Query()],
):
    # Query para buscar TODOs do usuário
    query = select(Todo).where(Todo.user_id == user.id)

    if filters.title:
        query = query.filter(Todo.title.contains(filters.title))

    if filters.description:
        query = query.filter(Todo.description.contains(filters.description))

    if filters.state:
        # Nao podemos usar o contains, pois o state é um Enum
        query = query.filter(Todo.state == filters.state)


    todos = session.scalars(query.offset(filters.offset).limit(filters.limit))

    return {'todos': todos.all()}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, user: CurrentUser, session: DBSession, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Todo not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        # model_dump: transforma um obj Pydantic em um dicionario
        # exclude_unset = True: ignora os campos None
        setattr(db_todo, key, value)  # db_todo.key = value

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, user: CurrentUser, session: DBSession):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Todo not found.'
        )

    session.delete(db_todo)
    session.commit()

    return {'message': 'Todo has been deleted successfully.'}
