from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()


router.register(prefix='auctions', viewset=views.AuctionViewSet, basename='auction')
router.register(prefix='products', viewset=views.ProductViewSet, basename='product')


urlpatterns = router.urls

