# Memory API

Backend API для приложения Memory — внешняя память для людей с афантазией.

Telegram Mini App + FastAPI бекенд на Oracle Cloud.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM для работы с БД
- **SQLite** — база данных
- **Pydantic** — валидация данных
- **Uvicorn** — ASGI сервер
- **Nginx** — reverse proxy
- **systemd** — управление сервисом

## Структура

- `main.py` — endpoints API
- `models.py` — модели БД (SQLAlchemy)
- `schemas.py` — Pydantic схемы для валидации
- `database.py` — подключение к БД

## Endpoints

### Люди
- `GET /api/people` — список людей
- `POST /api/people` — создать
- `GET /api/people/{id}` — получить одного
- `PATCH /api/people/{id}` — обновить
- `DELETE /api/people/{id}` — удалить

### События
- `GET /api/events` — список событий
- `POST /api/events` — создать
- `GET /api/events/{id}` — получить одно
- `PATCH /api/events/{id}` — обновить
- `DELETE /api/events/{id}` — удалить

### Истории
- `GET /api/stories` — список историй (фильтр `?status=active`)
- `POST /api/stories` — создать
- `GET /api/stories/{id}` — получить одну
- `PATCH /api/stories/{id}` — обновить
- `DELETE /api/stories/{id}` — удалить

### Системные
- `GET /api/health` — проверка работоспособности
- `GET /api/docs` — интерактивная документация (Swagger UI)

## Локальный запуск

```bash

