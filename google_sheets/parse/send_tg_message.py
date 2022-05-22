import telepot
from django.conf import settings


def send_message(data):
    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    text = 'Истек срок поставки: \n'
    # Формируем сообщение для отправки
    for order in data:
        text += (
            f'id: {order["first_id"]}|'
            f'заказ №:{order["second_id"]}|'
            f'стоимость,$: {order["price_usd"]}|'
            f'срок поставки: {order["date"]} \n\n'
        )
    bot.sendMessage(settings.TELEGRAM_SEND_TO_ID, text, parse_mode='Markdown')
