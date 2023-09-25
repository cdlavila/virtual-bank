import uuid
from django.db import models


# Create your models here.

# Loan model
class Loan(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    amount = models.FloatField(max_length=10000000)
    quotas = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "loans"
