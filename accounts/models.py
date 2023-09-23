import uuid
from django.db import models


# Create your models here.

# Account model
class Account(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=9999)
    balance = models.FloatField(default=0.0)
    withdraw_code = models.IntegerField(null=True)
    withdraw_code_expiration = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts"


# Transaction model
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'deposit'), ('withdraw', 'withdraw')],
                                        null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
