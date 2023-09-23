from rest_framework import routers
from django.urls import path
from .views import AccountRegisterView, AccountLoginView, AccountViewSet

urlpatterns = [
    path('api/v1/auth/register/', AccountRegisterView.as_view({'post': 'register'}), name='auth-register'),
    path('api/v1/auth/login/', AccountLoginView.as_view({'post': 'login'}), name='auth-login'),
]

router = routers.DefaultRouter()
router.register('api/v1/accounts', AccountViewSet, 'accounts')

urlpatterns += router.urls
