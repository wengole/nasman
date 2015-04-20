FROM python:3.4
MAINTAINER Ben Cole <wengole@gmail.com>

ENV PYTHONUNBUFFERED 1
COPY requirements.txt /srv/
WORKDIR /srv
# TODO: install zfs
# TODO: run migrations
# TODO: run manage.py sitetree_sync_apps
#RUN apt-get update -qq && apt-get install -y libpq-dev
RUN pip install -r requirements.txt
