from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_id', 'second_id', 'price_usd', 'price_rub', 'date')
    search_fields = ('second_id', 'date')
    list_filter = ('first_id', 'second_id', 'date')
