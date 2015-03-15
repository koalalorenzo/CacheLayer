FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
DELETE  /tmp/requirements.txt
ADD . /code
EXPOSE 8000
CMD uwsgi --ini /code/uwsgi.ini