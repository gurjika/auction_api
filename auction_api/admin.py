from django.contrib import admin
from . import models
# Register your models here.



admin.site.register(models.Auction)
admin.site.register(models.Product)
admin.site.register(models.AuctionItem)


