import datetime as dt

import gspread
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJob

from .models import Order
from .send_tg_message import send_message


def parse_ruble_exchange_rate():
    """
    Функцию чтобы каждый раз не запрашивать курс рубля
    Запрашиваем раз в пару минут и храним в настройках
    """
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    settings.RUBLE_EXCHANGE_RATE = data['Valute']['USD']['Value']


def parse_sheets():
    """
    Функция для парсинга данных из google sheets и сохранения их в базе данных
    :return:
    """
    google_acconts = gspread.service_account(filename='config/data/creads.json')
    sheets = google_acconts.open('Google api test task').sheet1
    records = sheets.get_all_records()
    # Получаем все заказы из бд
    all_order_in_db = Order.objects.all()
    expired = []
    for record in records:
        # Формуруем контекст для добавления\изменения в бд
        context = {
            'first_id': record.get('№'),
            'second_id': record.get('заказ №'),
            'price_usd': record.get('стоимость,$'),
            'price_rub': round(
                float(record.get('стоимость,$') * settings.RUBLE_EXCHANGE_RATE), 2
            ),
            'date': dt.datetime.strptime(
                record.get('срок поставки'), "%d.%m.%Y"
            ).date()
        }
        # Если истёк срок поставки, добавляем заказ в список
        if context['date'] < dt.date.today():
            expired.append(context)
        # Обновляем или создаем запись в базе данных..
        _, _ = Order.objects.update_or_create(
            first_id=context['first_id'], defaults=context
        )
        # Убираем из QuerySet заказы которые есть в Sheets
        all_order_in_db = all_order_in_db.exclude(first_id=context['first_id'])
    # Удаляем из бд все заказы которых не было в Sheets
    all_order_in_db.delete()
    # Отправляем сообщение в телеграм,
    # передаем туда все заказы с истекшим сроком поставки
    if len(expired):
        send_message(expired)


def start_scripts(seconds, minutes, hours):
    """
    Функция для запуска 2 задач,
    одна обновляет курс рубля,
    вторая парсит данные из Sheets
    :param seconds:
    :param minutes:
    :param hours:
    :return:
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # Запускаем поток с парсингом курса рубля раз в 10 минут
    scheduler.add_job(
        parse_ruble_exchange_rate,
        'interval',
        minutes=10,
        name='parse_exchange_rate',
        jobstore='default'
    )
    # Запускаем поток с парсингом таблицы
    scheduler.add_job(
        parse_sheets,
        'interval',
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        name='parse_sheets',
        jobstore='default'
    )
    scheduler.start()


def stop_scripts():
    """ Останавливаем все задачи путём удаления """
    DjangoJob.objects.all().delete()
