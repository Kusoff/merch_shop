from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'initiator',       # кто сделал заказ
            'status',          # статус заказа (создан/оплачен/доставлен)
            'created',         # дата создания
            'basket_history',  # содержимое корзины при оформлении
        )

