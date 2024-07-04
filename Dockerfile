FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y wait-for-it curl \
    && apt-get clean \
    && pip install --no-cache-dir --upgrade pip

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD sh -c "wait-for-it postgres:5432 -- python manage.py migrate && \
           python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='ermolich01@mail.ru').exists() or User.objects.create_superuser('ermolich01@mail.ru','Smurfeta228')\" && \
           python manage.py collectstatic --noinput && \
           gunicorn leagueverse.wsgi:application --bind 0.0.0.0:8000"
