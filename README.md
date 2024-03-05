# Social_Web

[![python](https://img.shields.io/badge/python-3.12_-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.109.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.25-critical?style=flat-square)](https://www.sqlalchemy.org//)
[![alembic](https://img.shields.io/badge/alembic-1.13.1_-violet?style=flat-square)](https://alembic.sqlalchemy.org//)


## Описание

Веб-приложение социальной сети, реализованное в виде микросервисов.
Реализовано 2 микросервиса: 
- auth_microservice(регистрация, аутентификация, авторизация, создание профиля, 
добавление\удаление\просмотр списка друзей, написание постов), паттерн репозиторий
- server_microservice(написание статей(сделано), лента новостей(в процессе), паттерн DDD
- Микросервисы соединены друг с другом через RabbitMQ.

## Стек
- FastAPI
- SQLAlchemy
- Alembic
- Postgresql
- Redis
- Rabbitmq