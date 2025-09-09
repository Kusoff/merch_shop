from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import RegisterView
from .views import (
    UsersViewSet, CategoryViewSet, ProductViewSet, BasketViewSet,
    DiscountViewSet, CommentsViewSet, CharacteristicViewSet, ProductImagesViewSet,
    OrderViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
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
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/', include(router.urls)),
]
