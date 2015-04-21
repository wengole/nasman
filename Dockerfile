FROM python:3.4
MAINTAINER Ben Cole <wengole@gmail.com>

# Install ZFS
RUN apt-get update -qq && apt-get install -y lsb-release
RUN wget http://archive.zfsonlinux.org/debian/pool/main/z/zfsonlinux/zfsonlinux_5_all.deb
RUN dpkg -i zfsonlinux_5_all.deb && rm zfsonlinux_5_all.deb
RUN apt-get update -qq && apt-get install -y debian-zfs

# Install python packages
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /srv/
WORKDIR /srv
RUN pip install -r requirements.txt
