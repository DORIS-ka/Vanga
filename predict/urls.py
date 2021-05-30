from rest_framework.routers import DefaultRouter

from predict import viewsets

router = DefaultRouter()
router.register('register', viewsets.CreateUserViewSet)
router.register('shop', viewsets.ShopViewSet)
router.register('category', viewsets.CategoryViewSet)
router.register('product', viewsets.ProductViewSet)

urlpatterns = router.urls
