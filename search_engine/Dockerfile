FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /

RUN python -m pip install --upgrade pip && \
    pip install -r /requirements.txt

COPY . /app/

ENTRYPOINT [ "python", "/app/__main__.py" ]
