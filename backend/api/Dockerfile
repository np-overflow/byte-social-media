FROM python:3.7.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /api
WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/

# change when in production
ENV DJANGO_DB_NAME=default
ENV DJANGO_SU_NAME=admin
ENV DJANGO_SU_EMAIL=admin@my.company
ENV DJANGO_SU_PASSWORD=mypass

CMD ["sh", "entrypoint.sh"]
