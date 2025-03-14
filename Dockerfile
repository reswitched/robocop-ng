FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /usr/src/app

COPY . .

# create a venv and set it to be used
RUN uv venv --no-config /uvvenv
ENV VIRTUAL_ENV=/uvvenv
ENV PATH="/uvvenv/bin:$PATH"

# install deps
RUN apk add --no-cache git gcc musl-dev python3-dev libffi-dev openssl-dev cargo && uv pip --no-config install . && apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo

WORKDIR /usr/src/app/robocop_ng

CMD [ "uv", "--no-config", "run", "--active", "python", "-m", "robocop_ng.__init__" ]