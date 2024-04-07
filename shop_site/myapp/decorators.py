from django.http import HttpResponseRedirect
from functools import wraps
from django.urls import reverse_lazy

def custom_login_required(view_func):
   @wraps(view_func)
   def wrapper(request, *args, **kwargs):
      if not request.user.is_authenticated:
         return HttpResponseRedirect(reverse_lazy('login'))
      return view_func(request, *args, **kwargs)
   return wrapper