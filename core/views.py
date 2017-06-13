from rest_framework import viewsets, permissions
from .serializers import CompanySerializer, ProductSerializer, UserSerializer, PermissionSerializer
from .models import Company, Product, Permission
from django.contrib.auth.models import User
from .permissions import IsCreatorOrContributor
from django.db.models import Q


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrContributor)

    def get_queryset(self):
        current_user = self.request.user
        my_permitted_companies = Permission.objects.filter(user=current_user).values_list('pk').distinct()
        my_companies = Q(pk__in=my_permitted_companies)
        return Company.objects.filter(my_companies)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    serializer_class = PermissionSerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrContributor)

    def get_queryset(self):
        current_user = self.request.user
        return Permission.objects.filter(user=current_user)

