from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('core.user', related_name='profile', on_delete=models.CASCADE)
    

class Auction(models.Model):
    status_active = models.BooleanField(default=False)
    starting_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='auctions')

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    seller = models.ForeignKey('Profile', related_name='products', on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name='auction_products', on_delete=models.SET_NULL, null=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products-images', default='default.jpg')


    