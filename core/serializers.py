from rest_framework import serializers
from .models import Inquiry, Company, Product


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'email', 'phone')


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='CompanyViewSet')

    class Meta:
        model = Product
        fields = ('title', 'company', 'image', 'description', 'product_type', 'unit_description', 'price_per_unit')


class InquirySerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='CompanyViewSet')

    class Meta:
        model = Inquiry
        fields = ('company', 'inquirer_email', 'is_anonymous')
