from datetime import datetime, timedelta
import random

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer, AccountDepositSerializer, AccountWithdrawSerializer


class AccountViewSet(viewsets.ModelViewSet):
    # Basic CRUD operations are already implemented by the ModelViewSet class
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer

    # Custom actions can be added to the ViewSet
    @action(detail=True, methods=['get'], url_path='balance')
    def get_balance(self, request, pk=None):
        # Custom logic here
        # Accesses the request data using request.data
        # Uses the 'pk' parameter to get the ID of the specific instance
        # Performs the operations and returns the desired response

        try:
            account = Account.objects.get(id_card=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=404)

        return Response({
            'balance': account.balance
        })

    @action(detail=True, methods=['patch'], url_path='deposit')
    def deposit(self, request, pk=None):
        amount = request.data['amount']
        serializer = AccountDepositSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=400)

        try:
            account = Account.objects.get(id_card=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=404)

        account.balance += amount
        account.save()
        return Response({
            'previous_balance': account.balance - amount,
            'amount_deposited': amount,
            'current_balance': account.balance
        })

    @action(detail=True, methods=['get'], url_path='withdraw_code')
    def generate_withdraw_code(self, request, pk=None):
        try:
            account = Account.objects.get(id_card=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=404)

        account.withdraw_code = random.randint(100000, 999999)
        account.withdraw_code_expiration = datetime.now() + timedelta(minutes=0.5)
        account.save()
        return Response({
            'withdraw_code': account.withdraw_code
        })

    @action(detail=True, methods=['patch'], url_path='withdraw')
    def withdraw(self, request, pk=None):
        amount = request.data['amount']
        withdraw_code = request.data['withdraw_code']
        serializer = AccountWithdrawSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=400)

        try:
            account = Account.objects.get(id_card=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=404)

        if account.withdraw_code != withdraw_code:
            return Response({'error': 'Invalid withdraw code'}, status=400)

        withdraw_code_expiration = account.withdraw_code_expiration.replace(tzinfo=None)

        if withdraw_code_expiration < datetime.now():
            return Response({'error': 'Withdraw code expired'}, status=400)

        account.balance -= amount
        account.withdraw_code = None
        account.withdraw_code_expiration = None
        account.save()
        return Response({
            'previous_balance': account.balance + amount,
            'amount_withdrawn': amount,
            'current_balance': account.balance
        })
