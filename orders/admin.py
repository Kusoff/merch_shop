from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'initiator', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('first_name', 'last_name', 'email', 'address', 'initiator__username')
    readonly_fields = ('basket_history', 'created')
    ordering = ('-created',)
