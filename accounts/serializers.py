from rest_framework import serializers
from django.core import validators
from .models import Account
from .hasher import hash_password


class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone', 'password', 'created_at')
        read_only_fields = ('created_at',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = hash_password(validated_data['password'])
        return super().create(validated_data)  # Call the pre-defined create method


class AccountLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=128)

    class Meta:
        fields = ('phone', 'password')


class AccountDepositSerializer(serializers.Serializer):
    amount = serializers.FloatField(validators=[validators.MinValueValidator(0.0)])

    class Meta:
        fields = ('amount',)
        extra_kwargs = {'amount': {'required': True}}


class AccountWithdrawSerializer(serializers.Serializer):
    amount = serializers.FloatField(validators=[validators.MinValueValidator(0.0)])
    withdraw_code = serializers.IntegerField(validators=[validators.MinValueValidator(100000)])

    class Meta:
        fields = ('amount', 'withdraw_code')
        extra_kwargs = {'amount': {'required': True}, 'withdraw_code': {'required': True}}
