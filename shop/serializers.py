from rest_framework import serializers
from .models import Users, Category, Characteristic, Product_Images, Product, Basket, Discount_For_Product_Category, \
    Comments
from orders.models import Order


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'phone', 'slug', 'birthday', 'is_verified_email', 'address', 'user_photo']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic_name', 'value']


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Images
        fields = ['id', 'img_name', 'img', 'first_img', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    product_photos = ProductImagesSerializer(many=True, read_only=True)
    product_characteristic = CharacteristicSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'first_price', 'discount', 'last_price', 'slug', 'description', 'category', 'stock',
            'available', 'created', 'updated', 'product_photos', 'product_characteristic'
        ]


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'product', 'quantity', 'created_timestamp', 'sum']


class DiscountSerializer(serializers.ModelSerializer):
    category_name = CategorySerializer(read_only=True)

    class Meta:
        model = Discount_For_Product_Category
        fields = ['id', 'category_name', 'discount_percentage', 'discount_start_date', 'discount_end_date', 'slug']


class CommentsSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'user', 'product', 'text', 'rating', 'date']


class OrderSerializer(serializers.ModelSerializer):
    initiator = UsersSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email', 'address', 'basket_history',
            'created', 'status', 'initiator'
        ]
