FROM python:3.4
MAINTAINER Ben Cole <wengole@gmail.com>

# Install ZFS
RUN apt-get update -qq && apt-get install -y lsb-release
RUN wget http://archive.zfsonlinux.org/debian/pool/main/z/zfsonlinux/zfsonlinux_5_all.deb
RUN dpkg -i zfsonlinux_5_all.deb && rm zfsonlinux_5_all.deb
RUN apt-get update -qq && apt-get install -y debian-zfs

# Make mountpoint for host filesystem
RUN mkdir /host_root

# Install python packages
ENV PYTHONUNBUFFERED 1
# Update pip and install some slow packages, to make updates to requirements faster to build
RUN pip install pip -U
RUN pip install tornado uwsgi pyyaml psycopg2 pyzmq
RUN pip install readline

COPY requirements.txt /root/
WORKDIR /root/
RUN pip install -r /root/requirements.txt
WORKDIR /srv
