from django.contrib.auth.models import User
from django.db import models

from w3.models import AccountMetamask


class Message(models.Model):
    objects = None
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    metamask = models.ForeignKey(AccountMetamask, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='metamask')
    metamask_to = models.CharField(max_length=250, null=True, blank=True)
    text = models.CharField(max_length=250)
    gas = models.IntegerField(default=0)
    gas_price = models.IntegerField(default=0)
    res_hash = models.CharField(max_length=250, null=True, blank=True)
    show = models.BooleanField(default=False)

