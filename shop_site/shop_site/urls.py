"""
URL configuration for shop_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import register, base, def_login, def_logout, create_product, Product_and_Searching, refund, approve_refund, reject_refund, purchase, make_purchase, create_refund, edit_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base, name='base'),
    path('register/', register, name='register'),
    path('sign_up/', def_login, name='login'),
    path('logout/', def_logout, name='logout'),
    path('product/', Product_and_Searching.as_view(), name='product_and_searching'),
    path('product/create_product/',create_product, name='create_product'),
    path('refunds/', refund, name='refund'),
    path('refunds/<int:refund_id>/approve/', approve_refund, name='approve_refund'),
    path('refunds/<int:refund_id>/reject/', reject_refund, name='reject_refund'),
    path('purchases/', purchase, name='purchase'),
    path('product/make_purchase/<int:product_id>', make_purchase, name='make_purchase'),
    path('refunds/create_refund/<int:purchase_id>', create_refund, name='create_refund'),
    path('product/edit_product/<int:product_id>', edit_product, name='edit_product')
]
