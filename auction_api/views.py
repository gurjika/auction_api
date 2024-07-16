from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from auction_api.models import Auction, Product
from auction_api.serializers import AuctionSerializer, ProductSerializer
# Create your views here.


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


    def get_serializer_context(self):
        return {'user': self.request.user}


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'user': self.request.user}
