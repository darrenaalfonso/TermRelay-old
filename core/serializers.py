from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Inquiry, Company, Product, Permission


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'date_joined')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'email', 'phone')


class PermissionSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = Permission
        fields = ('user', )


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='company-detail', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'company', 'image', 'description', 'product_type', 'unit_description', 'price_per_unit')


class InquirySerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='company-detail', read_only=True)

    class Meta:
        model = Inquiry
        fields = ('company', 'inquirer_email', 'is_anonymous')
