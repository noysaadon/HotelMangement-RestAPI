from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# Create your models here.

class AccountManager(BaseUserManager):

    def _create_user(self, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        if not first_name:
            raise ValueError("Users must have an first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name = first_name,
            last_name = last_name,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email,first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self,  email, first_name, last_name, password, **extra_fields):
        user = self._create_user( email, first_name, last_name,password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    username = models.CharField(max_length=100, unique=False, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.email