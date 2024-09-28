FROM python:3-alpine3.11

WORKDIR /app

COPY ./requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app/

ENTRYPOINT [ "python", "/app/__main__.py" ]
