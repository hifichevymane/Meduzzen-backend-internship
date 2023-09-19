FROM python:3.11.3-slim-buster

ENV PYTHONBUFFERED=1

# .env file variables
# https://stackoverflow.com/questions/30494050/how-do-i-pass-environment-variables-to-docker-containers
ENV SECRET_KEY=
ENV DEBUG=

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
