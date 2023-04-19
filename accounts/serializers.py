from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id_card', 'first_name', 'last_name', 'phone', 'password', 'balance', 'created_at')
        read_only_fields = ('created_at',)
        extra_kwargs = {'password': {'write_only': True}}
