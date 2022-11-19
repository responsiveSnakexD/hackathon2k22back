import uuid
from django.db import models
from authentication.user.models import User

# Create your models here.
class Campaign(models.Model):
    camapign_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    title       = models.CharField(max_length=50)
    start_date  = models.DateField()
    end_date    = models.DateField()

    def __str__(self):
        return self.title

class Tasks(models.Model):
    task_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    title           = models.CharField(max_length=100)
    description     = models.TextField()
    goal            = models.TextField()
    documentation   = models.TextField()
    xp              = models.SmallIntegerField(default=15)

    def __str__(self):
        return self.title

class CampaignsTasks(models.Model):
    campaign_task_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    task_id     = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    date        = models.DateField()

    def __str__(self):
        return str(self.date)

class UsersTasks(models.Model):
    campaign_task_id = models.ForeignKey(CampaignsTasks, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=70)
    is_submitted = models.BooleanField()
    is_verified = models.BooleanField()
    comment = models.TextField(blank=True, null=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['campaign_task_id', 'user_id', 'url'], name='unique_campaign_task_id_user_id_url_combination'
            )
        ]

    def __str__(self):
        return f'{self.user_id}({self.campaign_task_id}): {self.url}'
    
