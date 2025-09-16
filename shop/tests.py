from django.test import TestCase
from .models import Product, Category, Users, Product_Images, Discount_For_Product_Category, Basket
from django.contrib.auth import get_user_model, authenticate


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Тестовая категория')

    def test_last_price_with_discount(self):
        product = Product.objects.create(
            name='Товар со скидкой',
            first_price=1000,
            discount=20,
            category=self.category,
            stock=10,
        )
        self.assertEqual(product.last_price, 800, "Конечная цена должна быть 800 при скидке 20%")

    def test_last_price_without_discount(self):
        product = Product.objects.create(
            name='Товар без скидки',
            first_price=500,
            discount=0,
            category=self.category,
            stock=5,
        )
        self.assertEqual(product.last_price, 500, "Конечная цена должна быть равна первой цене, если скидка 0")

    def test_last_price_decimal_discount(self):
        product = Product.objects.create(
            name='Товар со скидкой 12.5%',
            first_price=400,
            discount=12.5,
            category=self.category,
            stock=5,
        )
        expected_price = int(400 * (1 - 12.5 / 100))
        self.assertEqual(product.last_price, expected_price,
                         "Конечная цена должна правильно считаться для дробной скидки")

    def test_str_method(self):
        product = Product.objects.create(
            name='Тестовый товар',
            first_price=100,
            discount=10,
            category=self.category,
            stock=2,
        )
        self.assertEqual(str(product), 'Тестовый товар', "__str__ должен возвращать имя продукта")


class SlugifyTestCase(TestCase):

    def test_user_slug(self):
        user = Users.objects.create(username='Test User')
        self.assertEqual(user.slug, 'test-user', "Slug для пользователя должен быть 'test-user'")

    def test_category_slug(self):
        category = Category.objects.create(name='Тестовая Категория')
        self.assertEqual(category.slug, 'тестовая-категория', "Slug для категории должен быть slugified")

    def test_product_images_slug(self):
        img = Product_Images.objects.create(img_name='Главная картинка')
        self.assertEqual(img.slug, 'главная-картинка', "Slug для изображения продукта должен быть slugified")

    def test_product_slug(self):
        category = Category.objects.create(name='Электроника')
        product = Product.objects.create(name='Смартфон X', first_price=1000, discount=10, category=category, stock=5)
        self.assertEqual(product.slug, 'смартфон-x', "Slug для продукта должен быть slugified")

    def test_discount_for_category_slug(self):
        category = Category.objects.create(name='Бытовая техника')
        discount = Discount_For_Product_Category.objects.create(
            category=category,
            discount_percentage=15,
            discount_end_date='2030-12-31'
        )
        self.assertEqual(discount.slug, 'бытовая-техника', "Slug для скидки по категории должен быть slugified")


Users = get_user_model()


class UserAuthTestCase(TestCase):

    def test_user_creation(self):
        user = Users.objects.create_user(username='ТестовыйПользователь', password='password123',
                                         email='test@example.com')
        self.assertEqual(user.username, 'ТестовыйПользователь')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(user.slug, 'тестовыйпользователь')  # проверка slug с кириллицей

    def test_authenticate_valid_user(self):
        user = Users.objects.create_user(username='user1', password='mypassword')
        authenticated_user = authenticate(username='user1', password='mypassword')
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, 'user1')

    def test_authenticate_invalid_password(self):
        Users.objects.create_user(username='user2', password='mypassword')
        authenticated_user = authenticate(username='user2', password='wrongpassword')
        self.assertIsNone(authenticated_user)

    def test_duplicate_username(self):
        Users.objects.create_user(username='duplicate', password='pass')
        with self.assertRaises(Exception):
            Users.objects.create_user(username='duplicate', password='pass2')

    def test_duplicate_email(self):
        Users.objects.create_user(username='user_email', email='email@test.com', password='pass')
        with self.assertRaises(Exception):
            Users.objects.create_user(username='user_email2', email='email@test.com', password='pass2')


class BasketTestCase(TestCase):

    def setUp(self):
        self.user = Users.objects.create_user(username='basketuser', password='123')
        self.category = Category.objects.create(name='Категория 1')
        self.product = Product.objects.create(
            name='Товар 1',
            first_price=1000,
            discount=10,
            category=self.category,
            stock=5
        )

    def test_create_or_update_basket(self):
        basket, created = Basket.create_or_update(product_id=self.product.id, user=self.user)
        self.assertTrue(created)
        self.assertEqual(basket.quantity, 1)

        basket2, created2 = Basket.create_or_update(product_id=self.product.id, user=self.user)
        self.assertFalse(created2)
        self.assertEqual(basket2.quantity, 2)

    def test_sum_and_total_quantity(self):
        basket, _ = Basket.create_or_update(product_id=self.product.id, user=self.user)
        basket.quantity = 3
        basket.save()
        self.assertEqual(basket.sum(), self.product.last_price * 3)
        self.assertEqual(Basket.objects.total_quantity(), 3)
        self.assertEqual(Basket.objects.total_sum(), self.product.last_price * 3)

    def test_de_json(self):
        basket, _ = Basket.create_or_update(product_id=self.product.id, user=self.user)
        data = basket.de_json()
        self.assertEqual(data['product_id'], self.product.id)
        self.assertEqual(data['quantity'], 1)
        self.assertEqual(data['price'], float(self.product.last_price))
