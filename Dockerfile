FROM ubuntu:16.04
 
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc
 
# Install python3
RUN  apt-get install -y python3 
 
# Install pip
RUN apt-get install -y wget vim \
    && wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py \
    && python3 /tmp/get-pip.py \
    && pip install --upgrade pip

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .