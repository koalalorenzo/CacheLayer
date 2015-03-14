FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt
CMD uwsgi --ini uwsgi.ini