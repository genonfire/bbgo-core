FROM python:3.10.13

ENV PYTHONUNBUFFERED 1
RUN mkdir /bbgo
WORKDIR /bbgo

ADD . /bbgo

RUN pip install -r requirements.txt
RUN pip install uwsgi
