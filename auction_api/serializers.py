from rest_framework import serializers

from auction_api.models import Auction, AuctionItem, Product, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'auctions']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price']

    def create(self, validated_data):
        obj = Product.objects.create(seller=self.context['user'].profile, **validated_data)
        return obj


class AuctionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionItem
        fields = ['id', 'product', 'quantity']


class AuctionSerializer(serializers.ModelSerializer):
    total_product_price = serializers.SerializerMethodField()
    auction_item = AuctionItemSerializer(many=True, required=False)
    status_active = serializers.BooleanField(read_only=True)
    starting_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    

    class Meta:
        model = Auction
        fields = ['id', 'status_active', 'starting_profile', 'auction_item', 'total_product_price']


    def get_total_product_price(self, obj):
        return obj.total_product_price


    def create(self, validated_data):

        obj = Auction.objects.create(starting_profile=self.context['user'].profile)
    
        for auction_item in validated_data['auction_item']:
            AuctionItem.objects.create(auction=obj, product=auction_item['product'], quantity=auction_item['quantity'])

        return obj