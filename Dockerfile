# Baixa imagem do Python 3.12 slim pelo DockerHub
FROM python:3.12-slim

# Impede que o Poetry crie um ambiente virtual
ENV POETRY_VIRTUALENVS_CREATE=false

# Cria o diretório app e define como diretório de trabalho
WORKDIR app/

# Copia o conteúdo do diretório atual para o diretório de trabalho
COPY . .

# Instala o Poetry
RUN pip install poetry

# Configura o número máximo de workers do Poetry para 10 (paralelismo da instalação)
RUN poetry config installer.max-workers 10

# Instala as dependências do projeto usando o Poetry
RUN poetry install --no-interaction --no-ansi

# Expõe a porta 8000 para acesso externo
EXPOSE 8000
CMD poetry run fastapi run fast_zero/app.py --host 0.0.0.0