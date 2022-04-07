FROM python:3.8.13

WORKDIR /code

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="${HOME}/.poetry/bin/:${PATH}"

RUN $HOME/.poetry/bin/poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /code/

RUN $HOME/.poetry/bin/poetry install --no-interaction --no-ansi --no-dev

COPY simple_weather_bot /code/simple_weather_bot
COPY docker_entrypoint.sh /code/

CMD ["./docker_entrypoint.sh"]
