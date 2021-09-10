# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /fastapi-app #set working directory to relative path

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app ./app

CMD [ "python", "app/main.py"] #tell Docker what command we want to run when our image is executed inside a containermake the application externally visible (i.e. from outside the container) by specifying --host=0.0.0.0.