from django.test import TestCase

from django.test import TestCase

from orders.models import Order
from shop.models import Users, Category, Product, Basket




class OrderTestCase(TestCase):

    def setUp(self):
        # Пользователь
        self.user = Users.objects.create_user(username='orderuser', password='12345')
        # Категория
        self.category = Category.objects.create(name='Электроника')
        # Продукты
        self.product1 = Product.objects.create(
            name='Телефон', first_price=1000, discount=10, category=self.category, stock=5
        )
        self.product2 = Product.objects.create(
            name='Ноутбук', first_price=5000, discount=20, category=self.category, stock=2
        )
        # Добавляем в корзину
        Basket.create_or_update(product_id=self.product1.id, user=self.user)
        Basket.create_or_update(product_id=self.product2.id, user=self.user)

    def test_order_creation(self):
        order = Order.objects.create(
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            address='ул. Пушкина, д. 10',
            initiator=self.user
        )
        self.assertEqual(order.initiator, self.user)
        self.assertEqual(order.status, Order.CREATED)
        self.assertEqual(order.first_name, 'Иван')

    def test_update_after_payment(self):
        order = Order.objects.create(
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            address='ул. Пушкина, д. 10',
            initiator=self.user
        )
        order.update_after_payment()
        self.assertEqual(order.status, Order.PAID)
        self.assertIn('purchased_items', order.basket_history)
        self.assertEqual(len(order.basket_history['purchased_items']), 2)
        # Проверяем, что корзина очищена
        self.assertEqual(Basket.objects.filter(user=self.user).count(), 0)
