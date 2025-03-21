from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from zero.database import get_session
from zero.models import Todo, User
from zero.schemas import FilterTodo, TodoList, TodoPublic, TodoSchema
from zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic, status_code=HTTPStatus.CREATED)
def create_post(todo: TodoSchema, user: CurrentUser, session: DBSession):
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
        query = query.filter(Todo.state.contains(filters.state))

    todos = session.scalars(query.offset(filters.offset).limit(filters.limit))
    
    return {'todos': todos.all()}