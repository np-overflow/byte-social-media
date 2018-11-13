#
# Dockerfile
# Scraper Container
# Build Specification
# 

FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    libgconf2-4 libnss3-1d libxss1 \
    fonts-liberation libappindicator1 xdg-utils \
    software-properties-common \
    curl unzip wget \
    xvfb

# install geckodriver and firefox
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver


RUN add-apt-repository -y ppa:ubuntu-mozilla-daily/ppa
RUN apt-get update && apt-get install -y firefox    

# Install python requirements
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

# Copy source code
COPY src /root/src

# Setup enviroment variables
ENV INSTAGRAM_USERNAME "j.l.i.m"
ENV INSTAGRAM_PASSWORD "superboy5"

# Run scraper
WORKDIR /root
CMD python3 src/scraper.py
