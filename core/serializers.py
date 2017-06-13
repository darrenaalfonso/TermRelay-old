from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Inquiry, Company, Product, Permission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'email', 'phone')

    def create(self, validated_data):
        company = Company.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone']
        )
        company.save()

        permission = Permission.objects.create(
            company=company,
            level="creator",
            user=self.context['request'].user
        )
        permission.save()

        return company


class PermissionSerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='company-detail',
                                                  queryset=Company.objects.all())
    # user = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail',
    #                                            queryset=User.objects.
    #                                            filter(pk=request.user.pk))

    class Meta:
        model = Permission
        fields = ('pk', 'user', 'company', 'level')


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='company-detail',
                                                  queryset=Company.objects.all())

    class Meta:
        model = Product
        fields = ('title', 'company', 'image', 'description', 'product_type', 'unit_description', 'price_per_unit')


class InquirySerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='company-detail',
                                                  queryset=Company.objects.all())

    class Meta:
        model = Inquiry
        fields = ('company', 'inquirer_email', 'is_anonymous')
