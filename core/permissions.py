from rest_framework import permissions
from .models import Permission, Company


class IsCreatorOrContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        if type(obj) is Company:
            try:
                permission = Permission.objects.get(company=obj, user=current_user)
                return True
            except Permission.DoesNotExist:
                return False
        else:
            try:
                permission = Permission.objects.get(company=obj.company, user=current_user)
                return True
            except Permission.DoesNotExist:
                return False
            except AttributeError:
                return False
        return False

