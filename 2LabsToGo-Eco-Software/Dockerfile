FROM python:3.9 as ocmanagerbase

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y

COPY requirements/base.txt /base_requirements.txt
RUN cat /base_requirements.txt | xargs pip install
