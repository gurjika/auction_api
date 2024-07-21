from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from auction_api.models import Auction, Product
from auction_api.serializers import AuctionSerializer, ProductSerializer
from django.db.models import Sum, F
from django.core.cache import cache

# Create your views here.


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.annotate(
        total_product_price=Sum(F('auction_item__product__price') * F('auction_item__quantity'))
    )
    serializer_class = AuctionSerializer

    def get_serializer_context(self):
        auction_pk = self.kwargs.get('pk')
        last_bid = cache.get(f'auction_{auction_pk}_bid')
        return {'user': self.request.user, 'last_bid': last_bid}




class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

    def get_serializer_context(self):
        return {'user': self.request.user}
