FROM python:3.7.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /api
WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/

# Create uwsgi user
RUN useradd --system -s /bin/false uwsgi
