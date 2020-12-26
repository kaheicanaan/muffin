FROM python:3.9

LABEL maintainer="Cherry Ng <cherry92@gmail.com>"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /server
EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --reload
