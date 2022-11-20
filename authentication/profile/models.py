import uuid
from django.db import models

from authentication.user.models import User


class UserProfile(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        db_table = "profile"
