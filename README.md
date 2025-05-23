# API для Библиотеки.

## Технологии:

- Python 3.8.10
- FastAPI 0.78.0
- PostgreSQL
- SQLAlchemy 1.4.41
- Jose 3.3.0
- Passlib 1.7.4
- Pydantic 1.10.2
- Alembic 1.7.7
- Pytest 7.1.2
- Flake8 7.1.2

## Установка PostgreSQL:

- [Скачайте установщик с официального сайта](https://www.postgresql.org/download/windows/)

## Настройка проекта (Windows):

1. Клонирование репозитория

```
git clone https://github.com/stallevdev/library_api.git
```

2. Переход в директорию library_api

```
cd library_api
```

3. Создание виртуального окружения

```
py -3.8 -m venv venv
```

4. Активация виртуального окружения

```
source venv/Scripts/activate
```

5. Обновите pip

```
python -m pip install --upgrade pip
```

6. Установка зависимостей

```
pip install -r requirements.txt
```

7. Создать файл .env

```
TITLE=API для Библиотеки
DESCRIPTION=REST API для управления книгами, читателями и выдачей книг. JWT-аутентификация.
DATABASE_URL=postgresql+psycopg2://postgres:Password@localhost:5432/library_db
SECRET_KEY=ваш_секретный_ключ
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=127.0.0.1
PORT=8080
```

8. Применение миграций

```
alembic upgrade head
```

9. Запуск проекта, введите команду

```
python -m app.main
```

10. [Локальная документация Swagger](http://127.0.0.1:8080/docs)

11. Остановка сервера

```
Ctrl + C
```

12. Запустите тесты

```
pytest
```

13. Деактивация виртуального окружения

```
deactivate
```
