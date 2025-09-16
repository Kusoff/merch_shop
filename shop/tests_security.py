from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from shop.models import Users, Product, Category, Basket
from orders.models import Order
from rest_framework_simplejwt.tokens import RefreshToken

User = Users


class BaseTestCase(APITestCase):
    def setUp(self):
        # Пользователи
        self.user1 = User.objects.create_user(username="user1", password="12345", email="user1@example.com")
        self.user2 = User.objects.create_user(username="user2", password="12345", email="user2@example.com")
        self.client = APIClient()

        # JWT-токены
        self.tokens = {
            self.user1: str(RefreshToken.for_user(self.user1).access_token),
            self.user2: str(RefreshToken.for_user(self.user2).access_token),
        }

        # Категория и продукты
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            first_price=100,
            last_price=100,
            description="Test description",
            category=self.category,
            stock=10
        )

        # Корзина
        Basket.objects.create(user=self.user1, product=self.product, quantity=2)

        # Заказ
        self.order = Order.objects.create(
            first_name='Ivan',
            last_name='Ivanov',
            email='ivan@test.com',
            address='ул. Пушкина, д. 1',
            initiator=self.user1
        )

    def auth(self, user):
        """Устанавливаем авторизацию пользователя"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokens[user]}')


class ProductAPITestCase(BaseTestCase):
    def test_admin_can_crud_products(self):
        url_list = reverse('products-list')

        # Обычный пользователь не может создавать
        self.auth(self.user1)
        response = self.client.post(url_list, {
            'name': 'Product2',
            'first_price': 500,
            'stock': 5,
            'category_id': self.category.id
        }, format='json')
        self.assertEqual(response.status_code, 403)

        # Админ создаёт продукт
        self.user2.is_staff = True
        self.user2.save()
        self.auth(self.user2)
        response = self.client.post(url_list, {
            'name': 'Product3',
            'first_price': 700,
            'stock': 3,
            'category_id': self.category.id
        }, format='json')
        self.assertEqual(response.status_code, 201)
        product_id = response.data['id']

        # Редактирование продукта
        url_detail = reverse('products-detail', args=[product_id])
        response = self.client.patch(url_detail, {'first_price': 750}, format='json')
        self.assertEqual(response.status_code, 200)

        # Обычный пользователь не может редактировать
        self.auth(self.user1)
        response = self.client.patch(url_detail, {'first_price': 800}, format='json')
        self.assertEqual(response.status_code, 403)

        # Проверка видимости продукта
        self.auth(self.user1)
        response = self.client.get(url_list)
        self.assertTrue(any(p['id'] == product_id for p in response.data))


class BasketOrderAPITestCase(BaseTestCase):
    def auth(self, user):
        """Удобный метод для авторизации пользователя в тестах"""
        token = str(RefreshToken.for_user(user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_basket_order_flow(self):
        self.auth(self.user1)

        # Проверяем корзину пользователя
        url_basket = reverse('basket-list')
        response = self.client.get(url_basket)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Детали заказа
        url_order_detail = reverse('orders-detail', args=[self.order.id])
        response = self.client.get(url_order_detail)
        self.assertEqual(response.status_code, 200)

        # Другой пользователь не должен иметь доступ
        self.auth(self.user2)
        response = self.client.get(url_order_detail)
        self.assertIn(response.status_code, [403, 404])

    def test_order_payment_updates(self):
        self.auth(self.user1)

        # Считаем сумму корзины до оплаты
        expected_total = float(Basket.objects.filter(user=self.user1).total_sum())

        # Обновляем статус оплаты
        self.order.update_after_payment()
        self.order.refresh_from_db()

        # Проверяем, что статус заказа изменился
        self.assertEqual(self.order.status, Order.PAID)

        # Проверяем сохранённую сумму в basket_history
        self.assertEqual(self.order.basket_history['total_sum'], expected_total)

        # Проверяем, что корзина пользователя теперь пустая
        self.assertEqual(Basket.objects.filter(user=self.user1).count(), 0)
