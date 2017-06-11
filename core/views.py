from rest_framework import viewsets, permissions
from .serializers import CompanySerializer, ProductSerializer, UserSerializer, PermissionSerializer
from .models import Company, Product, Permission
from django.contrib.auth.models import User


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (permissions.IsAuthenticated, )

