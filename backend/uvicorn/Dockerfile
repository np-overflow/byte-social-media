FROM python:3.7.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /websocket
WORKDIR /api
COPY requirements.txt /websocket/
RUN pip install -r /websocket/requirements.txt

ENTRYPOINT ["gunicorn", "-w 4", "-k uvicorn.workers.UvicornWorker", "-b=0.0.0.0:8000", "api.routing:application"]
