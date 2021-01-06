FROM ubuntu:18.04

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc python3-distutils
 
# Install python3
RUN apt-get install -y python3.6 
 
# Install pip
RUN apt-get install -y wget vim \
    && wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py \
    && python3.6 /tmp/get-pip.py \
    && pip install --upgrade pip
WORKDIR /code

COPY srequirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
