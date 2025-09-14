# Create your views here.
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Users, Category, Product, Basket, Discount_For_Product_Category, Comments, Characteristic, \
    Product_Images
from .serializers import (
    UsersSerializer, CategorySerializer, ProductSerializer, BasketSerializer,
    DiscountSerializer, CommentsSerializer, CharacteristicSerializer, ProductImagesSerializer,
    RegisterSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Админ видит всех
            return Users.objects.all()
        # Обычный пользователь видит только себя
        return Users.objects.filter(id=user.id)

    @extend_schema(description="Список всех пользователей (только для админов)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            # Создание и удаление разрешены только админам
            permission_classes = [IsAdminUser]
        else:
            # GET и PUT для своего профиля
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ppermission_classes = [AllowAny]


class BasketViewSet(viewsets.ModelViewSet):
    serializer_class = BasketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем корзину только для текущего пользователя
        return Basket.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Добавление товара в корзину
        product_id = request.data.get('product')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        basket, created = Basket.create_or_update(product_id, request.user)
        serializer = self.get_serializer(basket)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def increment(self, request, pk=None):
        # Увеличение количества товара
        basket = self.get_object()
        basket.quantity += 1
        basket.save()
        serializer = self.get_serializer(basket)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def decrement(self, request, pk=None):
        # Уменьшение количества товара или удаление
        basket = self.get_object()
        if basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
            serializer = self.get_serializer(basket)
            return Response(serializer.data)
        else:
            basket.delete()
            return Response({'status': 'deleted'})


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount_For_Product_Category.objects.all()
    serializer_class = DiscountSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer


class ProductImagesViewSet(viewsets.ModelViewSet):
    queryset = Product_Images.objects.all()
    serializer_class = ProductImagesSerializer


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="Регистрация нового пользователя",
        request=RegisterSerializer,
        responses=UsersSerializer
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        output_serializer = UsersSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
