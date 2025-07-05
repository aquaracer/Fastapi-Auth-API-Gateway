# API Gateway Auth Service

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115.12-green?logo=fastapi" />
  <img src="https://img.shields.io/badge/Docker-ready-blue?logo=docker" />
  <img src="https://img.shields.io/badge/PostgreSQL-16.2-blue?logo=postgresql" />
  <img src="https://img.shields.io/badge/Kafka-2.8.0-black?logo=apachekafka" />
  <img src="https://img.shields.io/badge/Poetry-dependencies-yellow?logo=python" />
  <img src="https://img.shields.io/badge/Alembic-migrations-orange?logo=alembic" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

---

## Описание

**API Gateway Auth Service** — это центральный шлюз (API Gateway) для аутентификации, управления пользователями и проксирования запросов к микросервисам профилей, фотографий и свайпов. Сервис реализован на FastAPI, поддерживает OAuth (Google, Яндекс), JWT, интеграцию с Kafka и PostgreSQL.

---

## Основные возможности

- Единая точка входа для клиентских приложений (API Gateway)
- Аутентификация через Google, Яндекс и по логину/паролю
- JWT-аутентификация
- Проксирование запросов к микросервисам профилей, фотографий, свайпов
- Интеграция с Kafka для событий свайпов
- Swagger/OpenAPI-документация
- Миграции БД через Alembic

---

## Архитектура

- **FastAPI** — основной web-фреймворк
- **PostgreSQL** — база данных пользователей
- **Kafka** — брокер событий для асинхронных операций
- **Docker** и **docker-compose** — контейнеризация
- **Nginx** — обратный прокси (опционально)
- **Alembic** — миграции схемы БД

<details>
<summary>Архитектурная схема (текст)</summary>

```
[Клиент]
   |
   v
[API Gateway (этот сервис)]
   |  |  |
   |  |  |---> [Микросервис профилей]
   |  |---> [Микросервис фотографий]
   |---> [Kafka] <--- [Микросервис свайпов]
   |
[PostgreSQL]
```
</details>

---

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone <your-repo-url>
cd auth_service
```

### 2. Настройте переменные окружения

Создайте файл `.env` в корне проекта (см. пример ниже).

<details>
<summary>Пример .env</summary>

```
PROJECT_NAME=Auth Service
VERSION=0.1.0
DEBUG=True
CORS_ALLOWED_ORIGINS=*

POSTGRES_HOST=db_auth
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DRIVER=postgresql+asyncpg
POSTGRES_DB=auth_service

JWT_SECRET_KEY=your_jwt_secret
JWT_ENCODE_ALGORITHM=HS256

GOOGLE_CLIENT_ID=...
GOOGLE_SECRET_KEY=...
GOOGLE_REDIRECT_URI=...
GOOGLE_TOKEN_URL=...
GOOGLE_USER_INFO_URL=...

YANDEX_CLIENT_ID=...
YANDEX_SECRET_KEY=...
YANDEX_REDIRECT_URI=...
YANDEX_TOKEN_URL=...
YANDEX_USER_INFO_URL=...

PROFILE_MICROSERVICE_BASE_URL=...
PROFILE_MICROSERVICE_USER_PROFILE_ENDPOINT=...
PROFILE_MICROSERVICE_USER_PROFILE_LIST_ENDPOINT=...

PHOTO_MICROSERVICE_BASE_URL=...
PHOTO_MICROSERVICE_PHOTO_ENDPOINT=...
PHOTO_MICROSERVICE_LIST_OWN_PHOTOS_ENDPOINT=...
PHOTO_MICROSERVICE_LIST_USERS_PHOTOS_ENDPOINT=...

SWIPE_MICROSERVICE_BASE_URL=...
PROCESS_SWIPES_TOPIC=process_swipes_topic
EVENT_TYPE_PROCESS_SWIPES=process_swipes
KAFKA_BROKER_ADDRESS=kafka:9093
```
</details>

### 3. Запуск через Docker Compose

```bash
docker-compose up --build
```
- Приложение: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Локальный запуск (без Docker)

```bash
pip install poetry
poetry install
poetry run uvicorn main:app --reload
```

### 5. Миграции базы данных

```bash
make migrate-create MIGRATION="your_message"
make migrate-apply
```

---

## Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST  | /auth         | Вход по логину/паролю |
| GET   | /auth/login/google | Редирект на Google OAuth |
| GET   | /auth/google  | Callback от Google OAuth |
| GET   | /auth/login/yandex | Редирект на Яндекс OAuth |
| GET   | /auth/yandex  | Callback от Яндекс OAuth |
| POST  | /user         | Регистрация пользователя |
| POST  | /user_profile | Создать профиль |
| GET   | /user_profile/list | Получить список профилей |
| PATCH | /user_profile | Обновить профиль |
| DELETE| /user_profile | Удалить профиль |
| POST  | /photo        | Загрузить фото |
| GET   | /photo/list_own_photos | Получить свои фото |
| GET   | /photo/list_users_photos | Получить фото других пользователей |
| DELETE| /photo/{photo_id} | Удалить фото |
| POST  | /swipes/process_swipes | Отправить событие свайпа (Kafka) |

---

## Технологии

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Kafka (aiokafka)
- Docker, docker-compose
- Poetry

---

## Разработка и тестирование

- Форматирование: `black`, `isort`
- Линтинг: `ruff`
- Тесты рекомендуется размещать в папке `tests/`

---

## Контакты

Автор: Boris Averin  
Email: 89068157313@mail.ru

---

# English version

## Description

**API Gateway Auth Service** is a central API Gateway for authentication, user management, and proxying requests to profile, photo, and swipe microservices. Built with FastAPI, supports OAuth (Google, Yandex), JWT, Kafka, and PostgreSQL.

## Features

- Single entry point for client apps (API Gateway)
- Authentication via Google, Yandex, and username/password
- JWT authentication
- Proxying requests to profile, photo, swipe microservices
- Kafka integration for swipe events
- Swagger/OpenAPI documentation
- DB migrations via Alembic

## Quick Start

1. Clone the repo and create a `.env` file (see example above)
2. Run with Docker Compose:
    ```bash
    docker-compose up --build
    ```
3. Or run locally:
    ```bash
    poetry install
    poetry run uvicorn main:app --reload
    ```
4. Run DB migrations:
    ```bash
    make migrate-create MIGRATION="your_message"
    make migrate-apply
    ```

## Main Endpoints

See the table above.

## Technologies

- Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Kafka, Docker, Poetry

---
