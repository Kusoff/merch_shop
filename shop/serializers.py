from rest_framework import serializers
from .models import Users, Category, Characteristic, Product_Images, Product, Basket, Discount_For_Product_Category, \
    Comments
from orders.models import Order


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id', 'username', 'email', 'phone', 'slug', 'birthday',
            'is_verified_email', 'address', 'user_photo', 'first_name', 'last_name'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ['username', 'password', 'phone', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)  # хэшируем пароль
        user.save()
        return user


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
    # Для POST будем принимать product_id
    product_id = serializers.IntegerField(write_only=True, required=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.last_price')
    sum = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product_id', 'product_name', 'product_price', 'quantity', 'sum')

    def get_sum(self, obj):
        return obj.sum()

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data.get('product_id')

        basket, created = Basket.create_or_update(product_id, user)
        return basket


class DiscountSerializer(serializers.ModelSerializer):
    category_name = CategorySerializer(read_only=True)

    class Meta:
        model = Discount_For_Product_Category
        fields = '__all__'
        read_only_fields = ['initiator', 'basket_history', 'status']

    def create(self, validated_data):
        validated_data['initiator'] = self.context['request'].user
        order = super().create(validated_data)
        # можно сразу сохранить корзину в history
        order.update_after_payment()
        return order


class CommentsSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'user', 'product', 'text', 'rating', 'created']


class OrderSerializer(serializers.ModelSerializer):
    initiator = UsersSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email', 'address', 'basket_history',
            'created', 'status', 'initiator'
        ]
