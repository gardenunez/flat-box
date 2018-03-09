FROM python:3.6

RUN apt-get update && apt-get install postgresql-client-9.4 -y

ARG uid=1000
ARG gid=1000
RUN addgroup --gid $gid flat-box
RUN useradd -m --uid $uid -g flat-box flat-box

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
ENV PYTHONPATH=/code
WORKDIR /code

ENV PYTHONPATH=/code
WORKDIR /code
