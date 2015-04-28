# CacheLayer
A basic cache layer as "proxy" for HTTP requests. Every call made to a specific URL provided are
redirected to a defined URL and cached/stored to provide a backup in case a service will not be available. It will prevent downtime using cache.

# How it works
The main use case is to provide a specific URL for specific API services or Open Data, that sometimes are down. The interface is built using AngularJS and Python Django with REST API, to provide a cleaner way to set it up. Through the web interface you can define the URL, the endpoints and the cache/storage settings in base of your needs.

1. Every time you will perform a HTTP request to the URL provided by CacheLayer, the same request will be executed to the URL specified when configuring it.
2. If the HTTP request is not valid, or a time-out error is raised, CacheLayer will try to provide the latest cache or storage available.
3. Once this is received, the response will be stored in the Redis database as back-up storage and for cache.

If you perform the same HTTP request, the system will check in the cache and provide that response, if the cache duration value is set as more than 0 seconds.

CacheLayer provides cache and storage. The Storage is meant to last for days or weeks, and is used only in case the URL specified does not answer back or is marked as "down". The cache instead is used to avoid multiple calls in a short period of time (seconds or minutes) to the same URL specified, and just provide the same response.

# How to run
To setup CacheLayer, you need [docker](http://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/). To build the CacheLayer containers you need to run:

    docker-compose build

Once built, you will need to set-up the database. To do so, run:

    docker-compose up -d
    docker-compose run uwsgi python ./manage.py migrate
    docker-compose restart uwsgi

In this way your CacheLayer image will be up and running and docker-compose will take care of setting up all the machines required.

Everything is up and running, now just visit the IP address of the machine running docker to get started. If you are using docker-machine on Mac OS X you can get that by running:

    open "http://$(docker-machine ip)"
