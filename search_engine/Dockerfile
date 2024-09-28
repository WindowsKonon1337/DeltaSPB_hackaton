FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app/

ENTRYPOINT [ "python", "/app/__main__.py" ]
