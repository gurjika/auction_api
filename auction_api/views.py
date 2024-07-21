from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from auction_api.models import Auction, Product, ProductImage
from auction_api.serializers import AuctionSerializer, ImageSerializer, ProductSerializer
from django.db.models import Sum, F
from django.core.cache import cache

# Create your views here.


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.annotate(
        total_product_price=Sum(F('auction_item__product__price') * F('auction_item__quantity'))
    )
    serializer_class = AuctionSerializer

    def get_serializer_context(self):
        context = {'user': self.request.user}
        auction_pk = self.kwargs.get('pk')
        if auction_pk:
            last_bid = cache.get(f'auction_{auction_pk}_bid')
            context.update({'last_bid': last_bid})
        return context




class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

    def get_serializer_context(self):
        return {'user': self.request.user}


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}