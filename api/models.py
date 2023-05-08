from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, password, **other_fields)

    def create_user(self, username, password, **other_fields):

        if not username:
            raise ValueError(_('You must provide a username'))

        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)
    
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    

class Request(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_receiver')
    declined = models.BooleanField(default=False, blank=True)
    accepted = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f'{self.sender.username} -> {self.reciever.username}'
    
class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users_friend')

    def __str__(self) -> str:
        return f'{self.user.username} and {self.friend.username}'