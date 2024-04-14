from django import forms
from django.contrib.auth import authenticate
from .models import Product, Refund, Wallet, Purchase
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) == 0:
            raise forms.ValidationError("Password cannot be empty")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Wallet.objects.create(user=user)
        return user



class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("User don't exist")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'cost', 'text', 'quantity']


class PurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Quantity')
    
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        super(PurchaseForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        wallet = Wallet.objects.get(user=self.user)
        
        if self.product.quantity < quantity:
            raise forms.ValidationError('There is no such amount of goods.')
        
        purchase_cost = quantity * self.product.cost
        if wallet.balance < purchase_cost:
            raise forms.ValidationError('There are not enough funds in your wallet.')
        
        return cleaned_data


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['cost','text','quantity']
