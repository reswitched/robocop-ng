FROM python:3.11-alpine

WORKDIR /usr/src/app

RUN python3 -m venv /poetryvenv && /poetryvenv/bin/pip install -U pip setuptools && /poetryvenv/bin/pip install poetry

COPY . .

WORKDIR /usr/src/app/robocop_ng

RUN apk add --no-cache git gcc musl-dev python3-dev libffi-dev openssl-dev cargo && /poetryvenv/bin/poetry install && apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo

CMD [ "/poetryvenv/bin/poetry", "run", "python", "-m", "robocop_ng" ]
