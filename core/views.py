from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from django.contrib.auth.models import User
from .permissions import IsCreatorOrContributor
from django.db.models import Q


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrContributor)

    def get_queryset(self):
        current_user = self.request.user
        permitted_companies = Permission.objects.filter(user=current_user).values_list('pk').distinct()
        companies = Q(pk__in=permitted_companies)
        return Company.objects.filter(companies)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        return serializer_class(*args, company_id=self.kwargs['company_id'], context=context, **kwargs)


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        current_user = self.request.user
        permitted_companies = Permission.objects.filter(user=current_user).values_list('pk').distinct()
        proposals = Q(company__in=permitted_companies)
        return Proposal.objects.filter(proposals)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    serializer_class = PermissionSerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrContributor)

    def get_queryset(self):
        current_user = self.request.user
        return Permission.objects.filter(user=current_user)

