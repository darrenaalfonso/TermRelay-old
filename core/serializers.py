from rest_framework import serializers
from .models import *


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

    def get_queryset(self):
        current_user = self.request.user
        my_permitted_companies = Permission.objects.filter(user=current_user).values_list('pk').distinct()
        my_companies = Q(pk__in=my_permitted_companies)
        return Company.objects.filter(my_companies)


class UserCompanyPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        current_user = self.context['request'].user
        my_permitted_companies = Permission.objects.filter(user=current_user).values_list('pk').distinct()
        my_companies = Q(pk__in=my_permitted_companies)
        return Company.objects.filter(my_companies)


class PermissionSerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)

    class Meta:
        model = Permission
        fields = ('pk', 'user', 'company', 'level')


class InquirySerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)
    inquirer = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', queryset=User.objects.all())

    class Meta:
        model = Inquiry
        fields = ('pk', 'company', 'inquirer_email', 'inquirer', 'is_anonymous', 'inquiry_date')


class ProposalTemplateSerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)
    creator = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', queryset=User.objects.all())

    class Meta:
        model = ProposalTemplate
        fields = ('pk', 'company', 'creator', 'creation_date')


class ProposalSerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)
    inquiry = serializers.HyperlinkedRelatedField(many=False, view_name='inquiry-detail',
                                                  queryset=Inquiry.objects.all())
    template = serializers.HyperlinkedRelatedField(many=False, view_name='proposaltemplate-detail',
                                                   queryset=ProposalTemplate.objects.all())
    users = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', queryset=User.objects.all())

    class Meta:
        model = Proposal
        fields = ('pk', 'company', 'inquiry', 'template', 'users', 'round', 'date')


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(many=False, view_name='company-detail',
                                                  queryset=Company.objects.all())

    class Meta:
        model = Product
        fields = ('pk', 'title', 'company', 'image', 'description', 'product_type', 'unit_description',
                  'price_per_unit')


class ProductQuestionSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(many=False, view_name='product-detail',
                                                  queryset=Product.objects.all())

    class Meta:
        model = ProductQuestion
        fields = ('pk', 'product', 'question')


class ProductQuestionChoiceSerializer(serializers.ModelSerializer):
    product_question = serializers.HyperlinkedRelatedField(many=False, view_name='productquestion-detail',
                                                           queryset=ProductQuestion.objects.all())

    class Meta:
        model = ProductQuestionChoice
        fields = ('pk', 'product_question', 'text_answer', 'numerical_answer', 'numerical_answer_units', 'description',
                  'notes')


class ProductRowSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(many=False, view_name='product-detail',
                                                  queryset=Product.objects.all())
    inquiry = serializers.HyperlinkedRelatedField(many=False, view_name='inquiry-detail',
                                                  queryset=Inquiry.objects.all())
    proposal = serializers.HyperlinkedRelatedField(many=False, view_name='proposal-detail',
                                                   queryset=Proposal.objects.all())
    proposal_template = serializers.HyperlinkedRelatedField(many=False, view_name='proposaltemplate-detail',
                                                            queryset=ProposalTemplate.objects.all())

    class Meta:
        model = ProductRow
        fields = ('pk', 'product', 'inquiry', 'proposal', 'proposal_template', 'quantity', 'price')


class ProductQuestionResponseSerializer(serializers.ModelSerializer):
    product_row = serializers.HyperlinkedRelatedField(many=False, view_name='productrow-detail',
                                                      queryset=ProductRow.objects.all())
    question = serializers.HyperlinkedRelatedField(many=False, view_name='question-detail',
                                                   queryset=ProductQuestion.objects.all())
    response = serializers.HyperlinkedRelatedField(many=False, view_name='productquestionchoice-detail',
                                                   queryset=ProductQuestionChoice.objects.all())

    class Meta:
        model = ProductQuestionResponse
        fields = ('pk', 'product_row', 'question', 'response')
