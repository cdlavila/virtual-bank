from rest_framework import routers
from django.urls import path
from .views import AccountRegisterView, AccountLoginView, AccountViewSet, TransactionViewSet

urlpatterns = [
    path('auth/register/', AccountRegisterView.as_view({'post': 'register'}), name='auth-register'),
    path('auth/login/', AccountLoginView.as_view({'post': 'login'}), name='auth-login'),
]

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet, 'accounts')
router.register('transactions', TransactionViewSet, 'transactions')

urlpatterns += router.urls
