from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, base_name='company')
router.register(r'products', views.ProductViewSet, base_name='product')
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'permissions', views.PermissionViewSet, base_name='permission')
router.register(r'proposals', views.ProposalViewSet, base_name='proposal')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
