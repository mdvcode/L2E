from django.contrib.auth.models import User
from django.db import models


class AccountMetamask(models.Model):
    objects = None
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    user_wallet_address = models.CharField(max_length=255)
    balance = models.FloatField(default=0)
    count_trans = models.IntegerField(default=0)

    def __str__(self):
        return self.user_wallet_address


class Transaction(models.Model):
    objects = None
    account = models.ForeignKey(AccountMetamask, null=True, blank=True, on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    res_hash = models.CharField(max_length=250, null=True, blank=True)
    data = models.CharField(max_length=5000, null=True, blank=True)


class IPFS(models.Model):
    objects = None
    file = models.FileField(null=True, blank=True)
    result_hash = models.CharField(max_length=250, null=True, blank=True)
    account = models.ForeignKey(AccountMetamask, null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=250, null=True, blank=True)
    hash_ipfs = models.CharField(max_length=250, null=True, blank=True)








    
