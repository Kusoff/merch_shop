from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Users, Category, Product, Basket, Discount_For_Product_Category, Comments, Characteristic, \
    Product_Images
from orders.models import Order
from .serializers import (
    UsersSerializer, CategorySerializer, ProductSerializer, BasketSerializer,
    DiscountSerializer, CommentsSerializer, CharacteristicSerializer, ProductImagesSerializer,
    OrderSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer


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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
