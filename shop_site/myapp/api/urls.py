from django.urls import path
from django.urls.conf import include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from myapp.api.resources import PurchaseApi, RefundApi, RegisterApi, ProductAndSearchingApi

router = routers.DefaultRouter()
router.register(r'products', ProductAndSearchingApi)
router.register(r'purchases', PurchaseApi)
router.register(r'refunds', RefundApi)

urlpatterns = [
   path('auth/', obtain_auth_token, name='auth_token'),
   path('register/', RegisterApi.as_view(), name='register'),
   path('', include(router.urls))
]