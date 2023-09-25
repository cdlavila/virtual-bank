from .models import Loan
from .serializers import LoanSerializer
from rest_framework import viewsets
from accounts.middlewares.auth import check_authentication


class LoanViewSet(viewsets.ModelViewSet):  # ModelViewSet is a generic view that provides CRUD operations
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @check_authentication
    def create(self, request, *args, **kwargs):
        self.request.data['account'] = request.user.get('id')
        return super(LoanViewSet, self).create(request, *args, **kwargs)

    @check_authentication
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(account=request.user.get('id'))
        return super(LoanViewSet, self).list(request, *args, **kwargs)

    @check_authentication
    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(account=request.user.get('id'))
        return super(LoanViewSet, self).retrieve(request, *args, **kwargs)

    @check_authentication
    def update(self, request, *args, **kwargs):
        self.request.data['account'] = request.user.get('id')
        self.queryset = self.queryset.filter(account=request.user.get('id'))
        return super(LoanViewSet, self).update(request, *args, **kwargs)

    @check_authentication
    def partial_update(self, request, *args, **kwargs):
        self.request.data['account'] = request.user.get('id')
        self.queryset = self.queryset.filter(account=request.user.get('id'))
        return super(LoanViewSet, self).partial_update(request, *args, **kwargs)

    @check_authentication
    def destroy(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(account=request.user.get('id'))
        return super(LoanViewSet, self).destroy(request, *args, **kwargs)
