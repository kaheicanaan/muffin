FROM python:3.9-slim-buster

LABEL maintainer="Cherry Ng <cherry92@gmail.com>"

RUN apt-get update
RUN apt-get -y install build-essential

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /server
EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --reload
