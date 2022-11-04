from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser, PermissionsMixin
)

# Register your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        
        user = self.model(
            email=email,
            username=username,
            date_joined = timezone.now(),
            is_superuser = 0,
            is_staff = 0,
            is_active = 1,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = 1
        user.is_staff = 1
        user.save(using=self._db)
        return user

class UserModel(AbstractUser, PermissionsMixin):

    class Meta:
        db_table = "my_user"
    
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.username
