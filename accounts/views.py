import random
from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import (AccountDepositSerializer, AccountWithdrawSerializer, AccountRegisterSerializer,
                          AccountLoginSerializer, TransactionSerializer)
from accounts.utils.hasher import verify_password
from accounts.utils import jwt
from accounts.middlewares.auth import check_authentication


class APIWelcomeView(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to the banking API'})


class AccountRegisterView(viewsets.GenericViewSet):
    serializer_class = AccountRegisterSerializer

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():  # Unique phone is validated in the serializer
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        account = serializer.save()
        token = jwt.create_token(data={'id': str(account.id)})

        return Response(
            {'id': account.id, 'token': token},
            status=status.HTTP_201_CREATED
        )


class AccountLoginView(viewsets.GenericViewSet):
    serializer_class = AccountLoginSerializer

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(phone=request.data['phone'])
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        is_math = verify_password(request.data['password'], account.password)
        if not is_math:
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        token = jwt.create_token(data={'id': str(account.id)})

        return Response(
            {'id': account.id, 'token': token},
            status=status.HTTP_200_OK
        )


class AccountViewSet(viewsets.GenericViewSet):
    # Custom actions can be added to the ViewSet
    @action(detail=False, methods=['get'], url_path='balance')
    @check_authentication
    def get_balance(self, request):
        # We can access the authenticated user with request.user
        pk = request.user.get('id')
        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'balance': account.balance
        })

    @action(detail=False, methods=['patch'], url_path='deposit')
    @check_authentication
    def deposit(self, request):
        amount = request.data.get('amount')
        pk = request.user.get('id')
        serializer = AccountDepositSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        account.balance += amount
        account.save()

        transaction = Transaction(account=account, amount=amount, transaction_type='deposit')
        transaction.save()

        return Response({
            'previous_balance': account.balance - amount,
            'amount_deposited': amount,
            'current_balance': account.balance,
            'transaction_id': transaction.id
        })

    @action(detail=False, methods=['get'], url_path='withdraw_code')
    @check_authentication
    def generate_withdraw_code(self, request):
        pk = request.user.get('id')
        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        account.withdraw_code = random.randint(100000, 999999)
        account.withdraw_code_expiration = datetime.now() + timedelta(minutes=0.5)
        account.save()
        return Response({
            'withdraw_code': account.withdraw_code
        })

    @action(detail=False, methods=['patch'], url_path='withdraw')
    @check_authentication
    def withdraw(self, request):
        amount = request.data.get('amount')
        pk = request.user.get('id')
        withdraw_code = request.data.get('withdraw_code')
        serializer = AccountWithdrawSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        if account.withdraw_code != withdraw_code:
            return Response({'error': 'Invalid withdraw code'}, status=status.HTTP_400_BAD_REQUEST)

        withdraw_code_expiration = account.withdraw_code_expiration.replace(tzinfo=None)

        if withdraw_code_expiration < datetime.now():
            return Response({'error': 'Withdraw code expired'}, status=status.HTTP_400_BAD_REQUEST)

        if account.balance < amount:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        account.balance -= amount
        account.withdraw_code = None
        account.withdraw_code_expiration = None
        account.save()

        transaction = Transaction(account=account, amount=amount, transaction_type='withdraw')
        transaction.save()

        return Response({
            'previous_balance': account.balance + amount,
            'amount_withdrawn': amount,
            'current_balance': account.balance,
            'transaction_id': transaction.id
        })


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @check_authentication
    def list(self, request, *args, **kwargs):
        pk = request.user.get('id')
        self.queryset = self.queryset.filter(account=pk)
        return super().list(request, *args, **kwargs)

    @check_authentication
    def retrieve(self, request, *args, **kwargs):
        pk = request.user.get('id')
        self.queryset = self.queryset.filter(account=pk)
        return super().retrieve(request, *args, **kwargs)
