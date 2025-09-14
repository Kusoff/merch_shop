from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from shop.models import Basket
from .models import Order
from rest_framework import serializers
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # админ видит все заказы
            return Order.objects.all()
        return Order.objects.filter(initiator=user)

    @extend_schema(description="Создать заказ с текущей корзиной пользователя")
    def perform_create(self, serializer):
        user = self.request.user
        baskets = Basket.objects.filter(user=user)

        if not baskets.exists():
            raise serializers.ValidationError("Cannot create an order with an empty basket.")

        basket_data = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum())
        }

        serializer.save(initiator=user, basket_history=basket_data)

        # Очищаем корзину после создания заказа
        baskets.delete()

    @extend_schema(description="Отметить заказ как оплачен (только админ)")
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_paid(self, request, pk=None):
        order = self.get_object()
        order.status = Order.PAID
        order.save()
        return Response({'status': 'paid'})

    @extend_schema(description="Отметить заказ как доставленный (только админ)")
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_delivered(self, request, pk=None):
        order = self.get_object()
        order.status = Order.DELIVERED
        order.save()
        return Response({'status': 'delivered'})

    @extend_schema(description="Отменить заказ (только создатель заказа)")
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()

        # Проверка: только инициатор или админ может отменять
        if order.initiator != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to cancel this order."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Нельзя отменить доставленный заказ
        if order.status == Order.DELIVERED:
            return Response(
                {"detail": "Cannot cancel a delivered order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Восстанавливаем товары в корзину только если отменяет сам пользователь
        if order.initiator == request.user:
            basket_data = order.basket_history.get("purchased_items", [])
            for item in basket_data:
                Basket.objects.create(
                    user=order.initiator,
                    product_id=item["product_id"],
                    quantity=item["quantity"]
                )

        order.status = Order.CANCELLED
        order.save()

        return Response({'status': 'cancelled'})
