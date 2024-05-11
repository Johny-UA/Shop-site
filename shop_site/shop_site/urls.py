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
from django.conf.urls.static import static
from django.urls import path, include
from myapp.views import RegisterView, BaseView, LoginView, LogoutView, CreateProductView, RefundView, ApproveRefundView, RejectRefundView, PurchaseView, MakePurchaseView, CreateRefundView, EditProductView, SuperuserRefundView, ProductListView
from shop_site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BaseView.as_view(), name='base'),
    path('register/', RegisterView.as_view(), name='register'),
    path('sign_up/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('product/', ProductListView.as_view(), name='product_and_searching'),
    path('product/create_product/', CreateProductView.as_view(), name='create_product'),
    path('refunds/', RefundView.as_view(), name='refund'),
    path('refunds/<int:refund_id>/approve/', ApproveRefundView.as_view(), name='approve_refund'),
    path('refunds/<int:refund_id>/reject/', RejectRefundView.as_view(), name='reject_refund'),
    path('purchases/', PurchaseView.as_view(), name='purchase'),
    path('product/make_purchase/<int:product_id>/', MakePurchaseView.as_view(), name='make_purchase'),
    path('refunds/create_refund/<int:purchase_id>/', CreateRefundView.as_view(), name='create_refund'),
    path('product/edit_product/<int:product_id>/', EditProductView.as_view(), name='edit_product'),
    path('refunds/superuser_refunds/', SuperuserRefundView.as_view(), name='superuser_refund'),
    path('api/', include('myapp.api.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)