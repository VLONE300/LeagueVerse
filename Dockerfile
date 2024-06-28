# Dockerfile

# Базовый образ
FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && apt-get clean

# Установка gunicorn
RUN pip install --no-cache-dir gunicorn

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt /app/

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . /app/

# Команда по умолчанию для запуска приложения
CMD ["gunicorn", "leagueverse.wsgi:application", "--bind", "0.0.0.0:8000"]
