from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()


router.register(prefix='auctions', viewset=views.AuctionViewSet, basename='auction')
router.register(prefix='products', viewset=views.ProductViewSet, basename='product')

images_router = routers.NestedDefaultRouter(parent_router=router, parent_prefix='products', lookup='product')
images_router.register(prefix='images', viewset=views.ImageViewSet, basename='image')

urlpatterns = router.urls + images_router.urls

