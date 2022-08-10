FROM python:3.10-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk add --no-cache git gcc musl-dev python3-dev libffi-dev openssl-dev cargo && pip install -U pip && pip install --no-cache-dir -r requirements.txt && apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo

COPY . .

WORKDIR /usr/src/app/robocop_ng

CMD [ "python", "./__init__.py" ]
