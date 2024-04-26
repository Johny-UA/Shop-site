from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator


from myapp.models import Product, Purchase, Refund, Wallet

class RegistrationSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True)

   class Meta:
      model = User
      fields = ['username', 'email','password']

   def validate(self, attrs):
      username = attrs.get('username')
      email = attrs.get('username')
      password = attrs.get('password')
      user_exist = Q(username__iexact=username)
      email_exist = Q(email__iexact=email)

      if User.objects.filter(user_exist).count():
         raise serializers.ValidationError("Username is already used")

      if User.objects.filter(email_exist).count():
         raise serializers.ValidationError("Email is already used")
      
      if len(password) <= 8:
         raise serializers.ValidationError("password must consist more than 8 symbols")
      
      return attrs
   
   def create(self, validated_data):
      return User.objects.create_user(**validated_data)


class ProductAndSearchingSerializer(serializers.ModelSerializer):

   class Meta:
      model = Product
      fields = ['id','name','text','cost','quantity']


class PurchaseSerializer(serializers.ModelSerializer):
   quantity = serializers.IntegerField(required=True, validators=[MinValueValidator(1)])

   class Meta:
      model = Purchase
      fields = ['id','product','quantity']

   def validate(self, attrs):
      product = attrs.get('product')
      user = self.context['request'].user
      wallet = Wallet.objects.get(user=user)
      quantity = attrs.get('quantity')
      if product.quantity < quantity:
         raise serializers.ValidationError("There is no such amount of goods.")
      if wallet.balance < product.cost * quantity:
         raise serializers.ValidationError("There are not enough funds in your wallet.")
      return attrs
      


class RefundSerializer(serializers.ModelSerializer):

   class Meta:
      model = Refund
      fields = ['id','purchase']

   def validate(self, attrs):
      user = self.context['request'].user
      purchase = attrs.get('purchase')
      if purchase.user != user:
         raise serializers.ValidationError("You haven't got this purchase.")
      return attrs