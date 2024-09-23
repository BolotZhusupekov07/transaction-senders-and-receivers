
# Transactions (Senders & Receivers) Backend
Project Language: Python 3.10

Project Framework: Django 5.1.1

### For convenince of whomever testing

I have created three users with each 3000 in the balance, ids:
1. 550e8400-e29b-41d4-a716-446655440010
2. 550e8400-e29b-41d4-a716-446655440011
3. 550e8400-e29b-41d4-a716-446655440010


### API docs

API docs is by /swagger


## Installation Steps:
```bash
git  clone

pip install poetry

poetry install

poetry shell

```


## Database Migrations
```bash
python manage.py migrate
```


## Running Server
```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py runserver
```

## Running Server with Docker Compose
```bash
docker compose -f docker/docker-compose.dev.yaml up --build
```


## Running Tests With Docker Compose
```bash
docker compose -f docker-compose.test.yaml up --build
```



## Architecture

**api** - contain logic for accepting request data and passing to schemas and services

**serializers** - contain logic for validating if request data is clean, exists and of proper format and shape.

**selectors** - reusable code that queries database

**services** - reusable code that delivers fine-grained business logic.

**models** - contain data and object presentation logic

**config** - project base settings folder


### Environment variables

| Name                                    | Description                                      | Default value |
| --------------------------------------- | ------------------------------------------------ | ------------- |
| DJANGO_SETTINGS_MODULE                              | Django Settings Environment to run the server with                                       | config.settings.dev            |
| SECRET_KEY                              | Secret key                                       | -             |
| DB_NAME                                 | Database name                                    | -             |
| DB_USER                                 | Database user                                    | -             |
| DB_PASSWORD                             | Database password                                | -             |
| DB_HOST                                 | Database host                                    | -             |
| DB_PORT                                 | Database port                                    | -             |
| DEBUG                                   | Debug mode                                       | True          |
| REDIS_HOST                              | Redis DB Host                                    | -             |
| REDIS_PORT                              | Redis DB Port                                    | 6379          |


## How create superadmin?

```shell
python manage.py createsuperuser
```