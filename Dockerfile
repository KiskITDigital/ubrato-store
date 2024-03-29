FROM python:3.11.6-alpine3.18

ARG SERVER_PORT=3000
ARG SERVER_ADDR=0.0.0.0
ARG S3_FOLDER=/files/
ARG JWT_SECRET

RUN export SERVER_PORT=${SERVER_PORT}
RUN export SERVER_ADDR=${SERVER_ADDR}
RUN export S3_FOLDER=${S3_FOLDER}

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100


RUN pip install poetry

WORKDIR /ubrato
COPY poetry.lock pyproject.toml /ubrato/

COPY ./app /ubrato/app
COPY ./scripts /ubrato/scripts

RUN poetry lock

RUN poetry install

RUN mkdir -p ${S3_FOLDER}

EXPOSE $SERVER_PORT

ENTRYPOINT [ "sh", "./scripts/run.sh" ]