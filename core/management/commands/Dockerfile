# core/management/commands/Dockerfile
FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y build-essential

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запуск бота
CMD ["python", "core/management/commands/bot.py"]