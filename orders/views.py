from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # показываем только заказы текущего пользователя
        return Order.objects.filter(initiator=self.request.user)

    def perform_create(self, serializer):
        # при создании заказа автоматически подставляем текущего пользователя
        serializer.save(initiator=self.request.user)
