from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import RegisterView
from .views import (
    UsersViewSet, CategoryViewSet, ProductViewSet, BasketViewSet,
    DiscountViewSet, CommentsViewSet, CharacteristicViewSet, ProductImagesViewSet,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'basket', BasketViewSet, basename='basket')
router.register(r'discounts', DiscountViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'characteristics', CharacteristicViewSet)
router.register(r'product-images', ProductImagesViewSet)

urlpatterns = [
    # JWT и регистрация
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),

    # Все маршруты через роутер
    path('', include(router.urls)),
]
