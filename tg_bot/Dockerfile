FROM python:3.11

WORKDIR /app/

COPY . /app/

RUN python -m pip install --upgrade pip && \
    pip install -r ./requirements.txt

ENTRYPOINT [ "python", "__main__.py" ]
