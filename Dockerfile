FROM python:3.8.13

WORKDIR /code

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="${PATH}:${HOME}/.poetry/bin/"

RUN ${HOME}/.poetry/bin/poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml docker_entrypoint.sh /code/

RUN ${HOME}/.poetry/bin/poetry install --no-interaction --no-ansi --no-dev

COPY simple_weather_bot /code/simple_weather_bot

CMD ["./docker_entrypoint.sh"]
