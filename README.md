# Parse-google-sheets-Django

## Описание

Скрипт для
парсинга [гугл таблицы(ссылка)](https://docs.google.com/spreadsheets/d/1FC3HcdKuND5rU3DgM_akQTe1pg2IpEmpg7ETQlBikiU/).

Реализовано:

* Получение данных из таблицы
* Парсинг курса рубля каждые 10 минут
* Сохранение данных в базе (postgresql)
* Настроена админка
* Скрипт работает в заданный интервал времени (hours, minutes, seconds)
* Проверка срока поставки, если срок поставки истёк отправляется уведомление в телеграм
* Бекенд с использованием Django. На главной выводится таблица со всеми заказами(Не реализован React)
* Реализован Docker

## Установка и запуск скриптов

1. Уставновить Docker и Docker-compose
2. Создать файл .env с переменными окружения в папке infra

```bash
SECRET_KEY = secret_key
TELEGRAM_TOKEN = token_bot # Если не указан будет использоваться мой тестовый акк
TELEGRAM_SEND_TO = id # Кому отправляем уведомление @userinfobot получить ид можно тут

# Данные от базы postgresql
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345678
DB_HOST=db
DB_PORT=5432
```

3. Сборка и запуск контейнера(Выполняется в папке infra)

```bash 
    docker-compose up -d --build
```

4. Сбор статики, применение миграций и создание суперпользователя(так же в папке infra)

```bash
  docker-compose exec web python manage.py collectstatic --noinput
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py createsuperuser
```

5. Запуск скриптов и доступные ссылки

Выполняется с адреса 127.0.0.1 или localhost

```bash
    localhost/ # Главная страница(Выводится таблица с заказами)
    localhost/admin # Админка
    localhost/start # будет запущено с интервалом 5 минут
    localhost/start?hours=1&minutes=1&seconds=1 # будет запущено с интервалом 1 час 1 минута 1 секунда
    localhost/start?seconds=1 # будет запущен с интервалом 5 минут 1 секунда
    localhost/start?hours=1 # будет запущен с интервалом 1 час 5 минут
    # При повторном переходе на данный адрес скрипты будут перезапущены
    # Нужно в случае если перестали работать
    localhost/stop # Выключает скрипты
```