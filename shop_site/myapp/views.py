from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic import ListView
from myapp.forms import RegistrationForm,AuthenticationForm, ProductForm, PurchaseForm, EditProductForm
from myapp.models import Product, Refund, Purchase, Wallet
from myapp.decorators import custom_login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.

class Product_and_Searching( ListView):
   model = Product
   template_name = 'product.html'
   context_object_name = 'products'

   @method_decorator(custom_login_required)
   def dispatch(self, *args, **kwargs):
      return super().dispatch(*args, **kwargs)

   def get_queryset(self):
      query = self.request.GET.get('search')
      if query:
         return Product.objects.filter(name__icontains=query)
      else:
         return Product.objects.all()

@custom_login_required
def create_product(request):
   if request.method == 'POST':
      form = ProductForm(request.POST)

      if form.is_valid():
         form.save()
         return HttpResponseRedirect(reverse_lazy('product_and_searching'))
      
   else:
      form = ProductForm()

   return render(request, 'create_product.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('base'))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def def_login(request):
   if request.method == 'POST':
         form = AuthenticationForm(request.POST)
         if form.is_valid():
            login(request, form.user)
            return HttpResponseRedirect('/')
   else:
      form = AuthenticationForm()

   return render(request, 'login.html', {'form': form})

def base(request):
   wallet = None
   if request.user.is_authenticated:
      wallet = Wallet.objects.get(user=request.user)
   return render(request, 'base.html', {'wallet' : wallet})

@custom_login_required
def def_logout(request):
   logout(request)
   return HttpResponseRedirect(reverse_lazy('base'))

@custom_login_required
def refund(request):
   if request.user.is_superuser:
      refund = Refund.objects.all()
   else:
      refund = Refund.objects.filter(purchase__user=request.user)
   return render(request, 'refund.html', {'refund': refund})

def approve_refund(request, refund_id):
    refund = get_object_or_404(Refund, pk=refund_id)

    if refund.approved == False:
        refund.approved = True
        refund.save()

        purchase = refund.purchase
        product = purchase.product
        user_wallet = Wallet.objects.get(user=purchase.user)

        user_wallet.balance += (purchase.quantity * product.cost)
        user_wallet.save()

        product.quantity += purchase.quantity
        product.save()

    return HttpResponseRedirect(reverse_lazy('refund'))

def reject_refund(request, refund_id):
    refund = Refund.objects.get(pk=refund_id)

    if not refund.approved:
        refund.delete()

    return HttpResponseRedirect(reverse_lazy('refund'))

@custom_login_required
def purchase(request):
   form = Purchase.objects.filter(user=request.user)
   return render(request, 'purchase.html', {'form' : form})

@custom_login_required
@transaction.atomic
def make_purchase(request, product_id):
   message = None
   product = get_object_or_404(Product, pk=product_id)
   if request.method == 'POST':
      form = PurchaseForm(request.POST)
      if form.is_valid():

         quantity = form.cleaned_data['quantity']
         wallet = Wallet.objects.get(user=request.user)

         if product.quantity >= quantity:

            purchase_cost = quantity * product.cost
            if wallet.balance >= purchase_cost:
               wallet.balance -= purchase_cost
               product.quantity -= quantity

               wallet.save()
               product.save()

               Purchase.objects.create(user=request.user ,product=product, quantity=quantity)

               return HttpResponseRedirect(reverse_lazy('product_and_searching'))

            else:
               message = 'There are not enough funds in your wallet.'
         else:
            message = 'There is no such amount of goods.'
   else:
      form = PurchaseForm()
   return render(request, 'make_purchase.html', {'form' : form,'product' : product , 'message' : message})

@custom_login_required
def create_refund(request, purchase_id):
   purchase = get_object_or_404(Purchase, pk=purchase_id)
   user_refund=Refund.objects.filter(purchase__user=request.user)
   if not user_refund.filter(purchase=purchase).exists():
      Refund.objects.create(purchase=purchase)
   else:
      messages.warning(request, 'This refund already exist.')
   return HttpResponseRedirect(reverse_lazy('purchase'))

@custom_login_required
def edit_product(request, product_id):
   product = get_object_or_404(Product, pk=product_id)
   if request.method == 'POST':
      form = EditProductForm(request.POST)
      if form.is_valid():
         cost = form.cleaned_data['cost']
         text = form.cleaned_data[ 'text' ]
         quantity = form.cleaned_data[ 'quantity' ]

         product.cost = cost
         product.text = text
         product.quantity = quantity
         product.save()

         return HttpResponseRedirect(reverse_lazy('product_and_searching'))
   else:
      form = EditProductForm()
   
   return render(request, 'edit_product.html', {'form': form, 'product' : product})