from django.db import models


# Create your models here.

# Account model
class Account(models.Model):
    id_card = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    password = models.CharField(max_length=9999)
    balance = models.FloatField(default=0.0)
    withdraw_code = models.IntegerField(null=True)
    withdraw_code_expiration = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts"
