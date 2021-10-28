FROM python:3.9.7-slim-buster

# Install Poetry
# ENV PYTHONPATH "/usr/src/app/:/usr/src/app/modules/"
ENV PATH="/root/.local/bin/:${PATH}"
ENV PYTHONPATH='./'
RUN apt-get update && apt-get install -y \
    curl


RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root

COPY incymo_backend/ .

CMD ["poetry", "run", "uvicorn", "incymo_backend.main:app", "--reload"]



# FROM python:3.9.7-slim-buster
# RUN mkdir /app
# COPY /incymo_backend /app
# COPY pyproject.toml poetry.lock /app 
# WORKDIR /app
# ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
# RUN pip3 install poetry
# RUN poetry config virtualenvs.create false
# RUN poetry install --no-root --no-dev

# COPY ./incymo_backend /app

# CMD ["poetry", "run", "uvicorn", "incymo_backend.main:app", "--reload"]




