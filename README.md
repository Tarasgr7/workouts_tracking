# Workout Training

## Опис

Workout Training — це бекенд на FastAPI для трекінгу  тренувань із базою даних PostgreSQL. Весь проєкт можна швидко запустити через Docker.

---

## Швидкий старт з Docker

### Крок 1. Клонування репозиторію

```bash
git clone https://github.com/Tarasgr7/workout_tracking.git
cd workout_training
````

### Крок 2. Запуск через Docker Compose

Переконайся, що у тебе встановлені [Docker](https://docs.docker.com/get-docker/) і [Docker Compose](https://docs.docker.com/compose/install/).

Запусти всі сервіси командою:

```bash
docker-compose up --build
```

Це підніме:

* FastAPI сервер (бекенд)
* PostgreSQL базу даних

### Крок 3. Очікуй, поки контейнери піднімуться

Коли сервер буде доступний, у консолі побачиш повідомлення типу:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Крок 4. Відкрий Swagger UI

В браузері зайди на [http://localhost:8000/docs](http://localhost:8000/docs), щоб переглянути та протестувати API.

---

## Важливо

* Усі налаштування бази (ім'я користувача, пароль, порт) прописані в `docker-compose.yml` та `.env` (якщо він є).
* Міграції бази автоматично застосовуються при запуску контейнера (якщо це передбачено твоїм Dockerfile або entrypoint).

---

## Зупинка проекту

Щоб вимкнути контейнери:

```bash
docker-compose down
```

---

## Технології

* Docker & Docker Compose
* Python 3.11+
* FastAPI
* PostgreSQL
* Alembic (міграції)

