FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN pip install -r /code/requirements.txt
CMD uwsgi --ini /code/uwsgi.ini