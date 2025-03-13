from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.get('/html', response_class=HTMLResponse)
def read_html():
    return """
    <html>
        <head>
            <title> Título Legal B( </title>
        </head>
        <body>
            <h1> Olá Mundo! </h1>
        </body>
    </html>"""
