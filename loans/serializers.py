from rest_framework import serializers
from django.core import validators
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(validators=[
        validators.MinValueValidator(0.0),
        validators.MaxValueValidator(10000000.0)
    ])
    quotas = serializers.IntegerField(validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(12)
    ])

    class Meta:
        model = Loan
        fields = '__all__'  # This will serialize all fields of the model
        extra_kwargs = {'amount': {'required': True}, 'quotas': {'required': True}}
