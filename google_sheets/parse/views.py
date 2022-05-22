from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django_apscheduler.models import DjangoJob

from . import services
from .models import Order


def index(request):
    order_list = Order.objects.all()
    price_sum = order_list.aggregate(
        total_usd=Sum('price_usd'),
        total_rub=Sum('price_rub')
    )
    return render(
        request,
        'index.html',
        context={'orders': order_list, 'price_sum': price_sum}
    )


def start_scripts(request):
    """
    Запускаем скрипты в фоновом режиме
    :param request:
    :return:
    """
    # Достаем из реквеста параметры для запуска скриптов,
    # если их нет применяем дефолтные
    seconds = request.GET.get('seconds', 0)
    minutes = request.GET.get('minutes', 5)
    hours = request.GET.get('hours', 0)
    # Вызываем 2 функции парсинга в первый раз руками,
    # т.к в следующий раз они запустятся только через то время, которое указали
    services.parse_ruble_exchange_rate()
    services.parse_sheets()
    # Если скрипты уже запущены то перезапускаем
    if DjangoJob.objects.all().count() >= 2:
        services.stop_scripts()
        services.start_scripts(int(seconds), int(minutes), int(hours))
        return HttpResponse('Скрипты перезапущенны')
    # Если нет, то просто запускаем
    services.start_scripts(int(seconds), int(minutes), int(hours))
    return HttpResponse('Скрипты запущены')


def stop_scripts(request):
    """
    Отключаем скрипты
    :return:
    """
    services.stop_scripts()
    return HttpResponse('Скрипты остановлены')
