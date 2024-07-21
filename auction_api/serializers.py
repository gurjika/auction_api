from rest_framework import serializers

from auction_api.models import Auction, AuctionItem, Product, ProductImage, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'auctions']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        required=False,
        write_only=True,
    )

    images = ImageSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'images', 'uploaded_images']

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images')
        obj = Product.objects.create(seller=self.context['user'].profile, **validated_data)
        for image in images:
            ProductImage.objects.create(image=image, product=obj)

        return obj


class AuctionItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = AuctionItem
        fields = ['id', 'product', 'quantity']


class AuctionSerializer(serializers.ModelSerializer):
    total_product_price = serializers.SerializerMethodField()
    auction_item = AuctionItemSerializer(many=True, required=False)
    status_active = serializers.BooleanField(read_only=True)
    starting_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    last_bid = serializers.SerializerMethodField()
    

    class Meta:
        model = Auction
        fields = ['id', 'status_active', 'starting_profile', 'auction_item', 'total_product_price', 'last_bid', 'starting_bid', 'finishing_bid']

    def get_last_bid(self, obj):
        last_bid = self.context.get('last_bid')
        return last_bid
    

    def get_total_product_price(self, obj):
        return obj.total_product_price


    def create(self, validated_data):

        obj = Auction.objects.create(starting_profile=self.context['user'].profile)
    
        for auction_item in validated_data['auction_item']:
            AuctionItem.objects.create(auction=obj, product=auction_item['product'], quantity=auction_item['quantity'])

        return obj