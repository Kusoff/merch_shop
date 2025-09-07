from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsersViewSet, CategoryViewSet, ProductViewSet, BasketViewSet,
    DiscountViewSet, CommentsViewSet, CharacteristicViewSet, ProductImagesViewSet,
    OrderViewSet
)

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'basket', BasketViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'characteristics', CharacteristicViewSet)
router.register(r'product-images', ProductImagesViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
