from django.contrib import admin
from .models import Product, Purchase, Refund, Wallet

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Product)
admin.site.register(Refund)
admin.site.register(Purchase)