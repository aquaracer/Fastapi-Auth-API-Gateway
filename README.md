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

**API Gateway Auth Service** — центральный шлюз (API Gateway) для аутентификации, управления пользователями и проксирования запросов к микросервисам профилей, фотографий и свайпов. Сервис реализован на FastAPI, поддерживает OAuth (Google, Яндекс), JWT, интеграцию с Kafka и PostgreSQL.

---

## 🚀 Основные возможности

- Единая точка входа для клиентских приложений (API Gateway)
- Аутентификация через Google, Яндекс и по логину/паролю
- JWT-аутентификация
- Проксирование запросов к микросервисам профилей, фотографий, свайпов
- Интеграция с Kafka для событий свайпов
- Swagger/OpenAPI-документация
- Миграции БД через Alembic

---

## 🛠️ Технологический стек

- **Фреймворк**: FastAPI
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy
- **Миграции**: Alembic
- **Контейнеризация**: Docker
- **Документация API**: Swagger UI
- **Управление пакетами**: Poetry

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

### Развертывание с помощью Docker

1. Создайте папку с проектом и склонируйте репозиторий:

```bash
mkdir Auth-API-Gateway
cd Auth-API-Gateway
git clone https://github.com/aquaracer/Fastapi-Auth-API-Gateway.git
```

2. Настройте переменные окружения в файле .env.

3. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

4. Примените миграции базы данных:

```bash
docker exec -it auth-api-gateway bash
poetry run alembic upgrade head
```

Приложение будет доступно по следующим адресам:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 Основные эндпоинты

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


