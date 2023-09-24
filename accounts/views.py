from datetime import datetime, timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Account
from .serializers import (AccountDepositSerializer, AccountWithdrawSerializer, AccountRegisterSerializer,
                          AccountLoginSerializer)
from .hasher import verify_password


class AccountRegisterView(viewsets.GenericViewSet):
    serializer_class = AccountRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can access this view

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():  # Unique phone is validated in the serializer
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        account = serializer.save()
        refresh = RefreshToken.for_user(account)
        access_token = str(refresh.access_token)

        return Response(
            {'id': account.id, 'access_token': access_token},
            status=status.HTTP_201_CREATED
        )


class AccountLoginView(viewsets.GenericViewSet):
    serializer_class = AccountLoginSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can access this view

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

        refresh = RefreshToken.for_user(account)
        access_token = str(refresh.access_token)

        return Response(
            {'id': account.id, 'access_token': access_token},
            status=status.HTTP_200_OK
        )


class AccountViewSet(viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    permission_classes = [permissions.AllowAny]  # Anyone can access this view

    # Custom actions can be added to the ViewSet
    @action(detail=True, methods=['get'], url_path='balance')
    def get_balance(self, request, pk=None):
        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'balance': account.balance
        })

    @action(detail=True, methods=['patch'], url_path='deposit')
    def deposit(self, request, pk=None):
        amount = request.data['amount']
        serializer = AccountDepositSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

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
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

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

        account.balance -= amount
        account.withdraw_code = None
        account.withdraw_code_expiration = None
        account.save()
        return Response({
            'previous_balance': account.balance + amount,
            'amount_withdrawn': amount,
            'current_balance': account.balance
        })
