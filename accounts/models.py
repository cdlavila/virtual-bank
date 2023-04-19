from django.db import models


# Create your models here.

# Account model
class Account(models.Model):
    id_card = models.IntegerField(max_length=9999999999)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=9999999999)
    password = models.CharField(max_length=9999)
    balance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts"
