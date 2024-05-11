from rest_framework.authentication import TokenAuthentication
from django.utils.timezone import now
from shop_site import settings
from rest_framework.exceptions import AuthenticationFailed


class TokenExpiredAuthentication(TokenAuthentication):

   def authenticate(self, request):
      try:
         user, token = super().authenticate()
      except TypeError:
         return 
      if (now() - token.created).seconds > settings.TOKEN_EXPIRE_SECONDS:
         token.delete()
         raise AuthenticationFailed("Token is already expired.")
      return user, token