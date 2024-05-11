from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import ProductForm, RegistrationForm, PurchaseForm, EditProductForm
from .models import Product, Refund, Wallet, Purchase

class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'products'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Product.objects.filter(name__icontains=query)
        else:
            return Product.objects.all()

class CreateProductView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('product_and_searching')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('base')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('base')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))

class BaseView(ListView):
    template_name = 'base.html'
    context_object_name = 'wallet'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Wallet.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallet'] = self.get_queryset()
        return context

class LogoutView(LoginRequiredMixin, CreateView):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('base'))

class RefundView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'refund.html'
    context_object_name = 'refund'

    def get_queryset(self):
        return Refund.objects.filter(purchase__user=self.request.user)

class SuperuserRefundView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'all_refund.html'
    context_object_name = 'all_refund'

    def get_queryset(self):
        return Refund.objects.all()

class ApproveRefundView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    def get(self, request, refund_id):
        refund = get_object_or_404(Refund, pk=refund_id)

        if not refund.approved:
            refund.approved = True
            refund.save()

            purchase = refund.purchase
            product = purchase.product
            user_wallet = Wallet.objects.get(user=purchase.user)

            user_wallet.balance += (purchase.quantity * product.cost)
            user_wallet.save()

            product.quantity += purchase.quantity
            product.save()

            refund.delete()
            purchase.purchase_is_returned = True
            purchase.save()

        return HttpResponseRedirect(reverse_lazy('refund'))

class RejectRefundView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    def get(self, request, refund_id):
        refund = get_object_or_404(Refund, pk=refund_id)

        if not refund.approved:
            refund.delete()

        return HttpResponseRedirect(reverse_lazy('refund'))

class PurchaseView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'purchase.html'
    context_object_name = 'form'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


class MakePurchaseView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = PurchaseForm
    template_name = 'make_purchase.html'

    @transaction.atomic
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        form = self.form_class(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            wallet = Wallet.objects.get(user=request.user)
            
            wallet.balance -= quantity * product.cost
            product.quantity -= quantity
            wallet.save()
            product.save()
            
            Purchase.objects.create(user=request.user, product=product, quantity=quantity)
            
            return HttpResponseRedirect(reverse_lazy('product_and_searching'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return context

class CreateRefundView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    def get(self, request, purchase_id):
        purchase = get_object_or_404(Purchase, pk=purchase_id)
        user_refund = Refund.objects.filter(purchase__user=request.user)
        if not user_refund.filter(purchase=purchase).exists():
            Refund.objects.create(purchase=purchase)
        else:
            messages.warning(request, 'This refund already exist.')
        return HttpResponseRedirect(reverse_lazy('purchase'))

class EditProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = EditProductForm
    template_name = 'edit_product.html'
    success_url = reverse_lazy('product_and_searching')
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['product_id'])

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        return super().form_valid(form)