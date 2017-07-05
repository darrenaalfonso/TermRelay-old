from rest_framework import serializers
from .models import *
from django.db.models import Q

global_company_id = 0


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
        fields = ('pk', 'name', 'email', 'phone')

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
        permitted_companies = Permission.objects.filter(user=current_user).values_list('pk').distinct()
        company_set = Q(pk__in=permitted_companies)
        return Company.objects.filter(company_set)


class UserPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        current_user = self.context['request'].user
        return User.objects.filter(username=current_user.username)


class CompanyProductField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        product_query = Q(company__pk=global_company_id)
        return Product.objects.filter(product_query)


class PermissionSerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)

    class Meta:
        model = Permission
        fields = ('pk', 'user', 'company', 'level')


class ProposalTemplateSerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)
    creator = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', queryset=User.objects.all())

    class Meta:
        model = ProposalTemplate
        fields = ('pk', 'company', 'creator', 'creation_date')


class ProductSerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)

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


class InquirySerializer(serializers.ModelSerializer):
    def __init__(self, *args, company_id=None, **kwargs):
        super(InquirySerializer, self).__init__(*args, **kwargs)
        company_set = Company.objects.filter(pk=company_id)
        self.fields['company'].queryset = company_set
        global global_company_id
        global_company_id = company_id

    company = serializers.HyperlinkedRelatedField(many=False,
                                                  view_name='company-detail',
                                                  queryset=Company.objects.all())
    inquirer = UserPKField(many=False)
    is_anonymous = serializers.BooleanField
    product_rows = CompanyProductField(many=True)

    class Meta:
        model = Inquiry
        fields = ('pk', 'company', 'inquirer_email', 'inquirer', 'is_anonymous', 'inquiry_date', 'product_rows',
                  'company_id')
        read_only_fields = ('inquirer', 'inquiry_date', 'company_id')


class ProposalSerializer(serializers.ModelSerializer):
    company = UserCompanyPKField(many=False)
    inquiry = serializers.HyperlinkedRelatedField(many=False, view_name='inquiry-detail',
                                                  queryset=Inquiry.objects.all())
    template = serializers.HyperlinkedRelatedField(many=False, view_name='proposaltemplate-detail',
                                                   queryset=ProposalTemplate.objects.all())
    users = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)

    class Meta:
        model = Proposal
        fields = ('pk', 'company', 'inquiry', 'template', 'users', 'round', 'date', 'product_rows')
        read_only_fields = ('users', 'round', 'date')