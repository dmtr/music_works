FROM python:3.8-alpine

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev git \
  && apk add postgresql-dev \
  && apk add libffi-dev py-cffi \
  && apk add postgresql-client \
  && pip3 install poetry

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./poetry.lock ${HOME}/
COPY ./pyproject.toml ${HOME}/

RUN poetry config virtualenvs.create false && poetry install

RUN mkdir /app
COPY . /app
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
