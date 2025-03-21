from fastapi import FastAPI

from zero.routers import auth, todos, users
from zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', response_model=Message)
def get_hello_world():
    return {'message': 'Hello World!'}
