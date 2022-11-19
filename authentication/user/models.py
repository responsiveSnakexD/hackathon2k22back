from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an e-mail adress')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email)
        )
        refresh = RefreshToken.for_user(user)
        user.refresh_token = str(refresh)
        user.access_token = str(refresh.access_token)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    refresh_token = models.TextField(unique=True)
    access_token = models.TextField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"""
{self.email}
{self.refresh_token}
{self.access_token}
    """

    class Meta:
        db_table = "user"
