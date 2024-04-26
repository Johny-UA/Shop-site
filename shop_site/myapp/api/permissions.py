from rest_framework.permissions import BasePermission 

class IsAdminReadOnly(BasePermission):
   

   def has_permission(self, request, view):
      return request.method in ['GET','HEAD'] or request.user.is_superuser
   

class IsAdminRefundActions(BasePermission):

   def has_permission(self, request, view):
      if view.action == 'approve' or view.action == 'reject':
         return request.user.is_superuser
      return request.user.is_authenticated
