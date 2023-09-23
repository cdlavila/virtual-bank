from rest_framework import serializers
from django.core import validators
from .models import Account


class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone', 'password', 'created_at')
        read_only_fields = ('created_at',)
        extra_kwargs = {'password': {'write_only': True}}


class AccountLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=128)

    class Meta:
        fields = ('phone', 'password')


class AccountDepositSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(validators=[validators.MinValueValidator(0.0)])

    class Meta:
        model = Account
        fields = ('amount',)
        extra_kwargs = {'amount': {'required': True}}


class AccountWithdrawSerializer(AccountDepositSerializer):
    amount = serializers.FloatField(validators=[validators.MinValueValidator(0.0)])
    withdraw_code = serializers.IntegerField(validators=[validators.MinValueValidator(100000)])

    class Meta:
        model = Account
        fields = ('amount', 'withdraw_code')
        extra_kwargs = {'amount': {'required': True}, 'withdraw_code': {'required': True}}
