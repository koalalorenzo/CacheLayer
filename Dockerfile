FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /code

ENV DJANGO_SETTINGS_MODULE=cachelayer.settings.docker
EXPOSE 8000
RUN rm -rf /code/staticfiles/*
RUN python /code/manage.py collectstatic --noinput
CMD uwsgi --ini /code/uwsgi.ini