#
# Dockerfile
# Scraper Container
# Build Specification
# 

FROM python:3.7-alpine

# Install Phantom JS
RUN apk update
RUN apk add --no-cache fontconfig curl && \
  mkdir -p /usr/share && \
  cd /usr/share \
  && curl -L https://github.com/Overbryd/docker-phantomjs-alpine/releases/download/2.11/phantomjs-alpine-x86_64.tar.bz2 | tar xj \
  && ln -s /usr/share/phantomjs/phantomjs /usr/bin/phantomjs

# Install python requirements
COPY requirements.txt /root/requirements.txt
RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /root/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Copy source code
COPY src /root

# Run scraper
WORKDIR /root
CMD python scraper.py
