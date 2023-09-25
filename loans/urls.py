from rest_framework import routers
from .views import LoanViewSet


router = routers.DefaultRouter()
router.register('loans', LoanViewSet, 'loans')

urlpatterns = router.urls
