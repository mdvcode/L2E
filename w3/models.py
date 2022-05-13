from django.contrib.auth.models import User
from django.db import models


class AccountMetamask(models.Model):
    objects = None
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    user_wallet_address = models.CharField(max_length=255)
    private_key = models.CharField(max_length=255)
    balance = models.FloatField(default=0)
    count_trans = models.IntegerField(default=0)


class Transaction(models.Model):
    objects = None
    account = models.ForeignKey(AccountMetamask, null=True, blank=True, on_delete=models.CASCADE)
    to_account = models.CharField(max_length=250)
    gas = models.IntegerField(default=0)
    value = models.FloatField(default=0)
    gas_price = models.IntegerField(default=0)
    res_hash = models.CharField(max_length=250, null=True, blank=True)
    data = models.CharField(max_length=250, null=True, blank=True)
    text = models.CharField(max_length=250, null=True, blank=True)

    
