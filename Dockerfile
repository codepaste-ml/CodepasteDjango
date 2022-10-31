FROM python:3.7-alpine

EXPOSE 8000

RUN apk update && apk add postgresql-dev gcc python3-dev libffi-dev musl-dev libc-dev

RUN pip install pipenv

WORKDIR app

COPY Pipfile /app
COPY Pipfile.lock /app

RUN set -ex && pipenv install --deploy --system

COPY . /app

RUN chmod +x docker-entrypoint.sh
CMD ["sh", "docker-entrypoint.sh"]
