![](https://github.com/yurlovaviktoriya/foodgram-project/workflows/Foodgram%20workflow/badge.svg)

# Foodgram-project
Foodgram-project is a database of recipes. Users can post recipes and add recipes to their shopping list. The service will generate a summary report of the required ingredients. Users can subscribe to interesting authors and add their recipes to favorites.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine using [Docker Compose](https://docs.docker.com/compose/).


### Prerequisites

What things you need to install the software and how to install them.

 - [Docker](https://docs.docker.com/engine/install/);
 - [Docker Compose](https://docs.docker.com/compose/install/).
 
 ### Installing
Application launch:
```
docker-compose up
```  
See container id
```
docker ps
```
Open web container
```
docker exec -it <CONTAINER ID> bash
```
Perform migrations
```
python manage.py migrate
```
Сreate superuser
```
python manage.py createsuperuser
```  
Import data into DB
```
python manage.py loaddata ./recipes/fixtures/ingredients.json
```

    python manage.py loaddata ./recipes/fixtures/tags.json

## Built With

-   [Django](https://www.djangoproject.com/) is a high-level Python Web framework;
- [PostgreSQL](https://www.postgresql.org/) is a powerful, open source object-relational database system.
- [Gunicorn](https://gunicorn.org/) is a Python WSGI HTTP Server for UNIX.
- [Nginx](https://nginx.org/) is an HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy server.


## Authors
[**Yurlova Viktoriya**](https://github.com/yurlovaviktoriya) is a student of [Yandex.Praktikum](https://praktikum.yandex.ru/).   This project is the graduation thesis for the [Python-developer preparation program](https://praktikum.yandex.ru/backend-developer/).
