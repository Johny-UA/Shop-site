from rest_framework.generics import CreateAPIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from myapp.api.serializers import ProductAndSearchingSerializer, PurchaseSerializer, RefundSerializer, RegistrationSerializer
from myapp.models import Product, Purchase, Refund, Wallet
from myapp.api.permissions import IsAdminReadOnly, IsAdminRefundActions
from django.db.models import Q
from django.db import transaction

class RegisterApi(CreateAPIView):
   serializer_class = RegistrationSerializer
   permissions_classes = []
   queryset = User.objects.all()


class ProductAndSearchingApi(viewsets.ModelViewSet):
   queryset = Product.objects.all()
   serializer_class = ProductAndSearchingSerializer
   http_method_names = ['get','post','patch']
   permission_classes = [IsAdminReadOnly]


class PurchaseApi(viewsets.ModelViewSet):
   queryset = Purchase.objects.all()
   serializer_class = PurchaseSerializer
   http_method_names = ['get','post']

   def get_queryset(self):
      return Purchase.objects.filter(user=self.request.user)
   
   def perform_create(self, serializer):
      product = serializer.validated_data['product']
      wallet = Wallet.objects.get(user=self.request.user)
      quantity = serializer.validated_data['quantity']
      product.quantity -= quantity
      wallet.balance -= quantity * product.cost
      with transaction.atomic():
         product.save()
         wallet.save()
      return serializer.save(user=self.request.user)


class RefundApi(viewsets.ModelViewSet):
   queryset = Refund.objects.all()
   serializer_class = RefundSerializer
   http_method_names = ['get','post']
   permission_classes = [IsAdminRefundActions]

   def get_queryset(self):
      query = Q()
      if not self.request.user.is_superuser:
         query |= Q(purchase__user=self.request.user)
      return Refund.objects.filter(query)

   @action(methods=['post'], detail=True)
   def approve(self, request, pk=None):
      ret = self.get_object()
      purchase = ret.purchase
      wallet = Wallet.objects.get(user=purchase.user)
      product = purchase.product
      quantity = purchase.quantity
      cost = product.cost
      wallet.balance += quantity * cost
      product.quantity += quantity
      with transaction.atomic():
         wallet.save()
         product.save()
         ret.delete()
         purchase.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

   @action(methods=['post'], detail=True)
   def reject(self, request, pk=None):
      ret = self.get_object()
      ret.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)


