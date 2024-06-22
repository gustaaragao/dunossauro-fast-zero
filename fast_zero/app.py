from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!!'}


@app.get('/html', response_class=HTMLResponse)
def read_html():
    return "<html><h1>Olá mundo!!</h1></html>"
