"""
models for different users
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    PermissionsMixin,
    BaseUserManager
)


class UserManager(BaseUserManager):
    """customized User manager."""

    def create_user(self, username, password, **kwargs):
        """create and save a normal user"""
        # print(email)
        # print(password)
        # print(kwargs)
        if not username:
            raise ValueError('user must have an email address')
        user = self.model(email=self.username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **kwargs):
        """create a superuser"""
        user = self.create_user(username, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractUser, PermissionsMixin):
    """user in the system"""
    username = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        """returns username as identification"""
        return str(self.username)





