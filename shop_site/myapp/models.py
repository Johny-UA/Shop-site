from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

# Create your models here.

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

    def __str__(self) -> str:
       return f"{self.user}'s wallet"


class Product(models.Model):
   name = models.CharField(max_length=100,
                           null=False,
                           blank=False)

   cost = models.IntegerField(default=1)
   
   text = models.TextField(blank=True)

   quantity = models.IntegerField(default=1)

   def __str__(self):
      return self.name



class Purchase(models.Model):
   user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

   product = models.ForeignKey(Product,
                              on_delete=models.DO_NOTHING)
   
   quantity = models.IntegerField(default=1)

   purchase_time = models.DateTimeField(auto_now_add=True)

   def __str__(self) -> str:
      return f"{self.user.username} - {self.product.name}"


class Refund(models.Model):
   purchase = models.ForeignKey(Purchase, 
                                 on_delete=models.DO_NOTHING)

   refunds_time = models.DateTimeField(auto_now_add=True)

   approved = models.BooleanField(default=False)

   def __str__(self) -> str:
      return f'Refund {self.purchase}'