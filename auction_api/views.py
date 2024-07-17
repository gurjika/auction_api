from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from auction_api.models import Auction, Product
from auction_api.serializers import AuctionSerializer, ProductSerializer
from django.db.models import Sum, F
# Create your views here.


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.annotate(
        total_product_price=Sum(F('auction_item__product__price') * F('auction_item__quantity'))
    )
    serializer_class = AuctionSerializer


    def get_serializer_context(self):
        return {'user': self.request.user}


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'user': self.request.user}
