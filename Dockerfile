FROM python:3.10-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='ermolich01@mail.ru').exists() or User.objects.create_superuser('ermolich01@mail.ru','Smurfeta228')"
    && python manage.py runserver 0.0.0.0:8000


## Установка зависимостей
#RUN apt-get update \
#    && apt-get install -y libpq-dev gcc \
#    && apt-get clean
#
## Установка gunicorn
#RUN pip install --no-cache-dir gunicorn
#
## Установка рабочей директории
#WORKDIR /app
#
## Копирование зависимостей
#COPY requirements.txt /app/
#
## Установка зависимостей Python
#RUN pip install --no-cache-dir -r requirements.txt
#
## Копирование остальных файлов проекта
#COPY . /app/
#
## Команда по умолчанию для запуска приложения
#CMD ["gunicorn", "leagueverse.wsgi:application", "--bind", "0.0.0.0:8000"]
