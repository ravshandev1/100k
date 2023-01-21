from django.contrib import admin
from .models import Order, Stream


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'name', 'phone', 'product', 'created_at']


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['orders']
