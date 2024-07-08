from typing import Any
from django.db import models
from account.models import User
from django.contrib.auth.models import BaseUserManager


class TransactionManager(models.Manager):
    """customizing transactions creations"""

    def create(self, **kwargs: Any) -> Any:
        
        temp = super().create(**kwargs)
        user = kwargs['user']
        user.get_credit
        
        return temp


class Transaction(models.Model):
    """registering all transactions for a wallet"""
    transaction_mode = (
        ('+', 'charge'),
        ('-', 'cunsumption')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now=True)
    mode = models.CharField(choices=transaction_mode, max_length=255, default='+')
    mount = models.PositiveIntegerField(default=0)
    objects = TransactionManager()

    def __str__(self):
        """returns a human readable string"""
        return f'{self.user.username} --> {self.mode}{self.mount}'
    
    





