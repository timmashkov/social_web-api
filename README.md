# Social_Web

[![python](https://img.shields.io/badge/python-3.12_-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.109.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.25-critical?style=flat-square)](https://www.sqlalchemy.org//)
[![alembic](https://img.shields.io/badge/alembic-1.13.1_-violet?style=flat-square)](https://alembic.sqlalchemy.org//)


## Фичи

Веб-приложение социальной сети, реализованное в виде микросервисов.
Реализовано 2 микросервиса: 
- auth_microservice(регистрация, аутентификация, авторизация, создание профиля, написание постов, создание групп,
добавление\удаление\просмотр списка друзей, постов, групп, админка), паттерн репозиторий
- server_microservice(создание статей, мероприятий, гостей и билетов, лента новостей, паттерн DDD
- Микросервисы соединены друг с другом через RabbitMQ.

## Стек
- FastAPI
- SQLAlchemy
- Alembic
- Postgresql
- Redis
- Rabbitmq

## Описание

Связь микросервисов осуществляется с помощью aio-pika,
в первом микросервисе класс рэббита и класс rpc находятся в
auth_microservice/src/configuration/broker.py. Во втором в 
server_microservice/app_src/infrastructure/broker/rabbit_handler.py
Подключение к рэббиту выполняется при старте каждого микросервиса,
путем lifespan. Реализация rpc.call() следующая:

- В сервисе новостей (server_microservice/app_src/services/feed_service.py)
происходит вызов функции возврата списка профилей и групп в другом
микросервисе.

