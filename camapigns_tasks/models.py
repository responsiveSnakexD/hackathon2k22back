from django.db.models.signals import post_save
from django.db import models
from authentication.user.models import User

# Create your models here.


class Campaign(models.Model):
    camapign_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.TextField()
    documentation = models.TextField()
    xp = models.SmallIntegerField(default=15)
    is_bigtask = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CampaignsTasks(models.Model):
    campaign_task_id = models.AutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class UsersTasks(models.Model):
    campaign_task_id = models.ForeignKey(
        CampaignsTasks, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=70)
    is_submitted = models.BooleanField()
    is_verified = models.BooleanField()
    comment = models.TextField(blank=True, null=False)

    __old_is_verified = False

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['campaign_task_id', 'user_id', 'url'], name='unique_campaign_task_id_user_id_url_combination'
            )
        ]

    def __str__(self):
        return f'{self.user_id}({self.campaign_task_id}): {self.url}'

    # def check_xp(self, **kwargs):
    #     print("Hello World")
    #     if self.is_verified:
    #         print(xp_for_task)
    #         self.user_id.update(current_xp=10)
    # post_save.connect(check)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_is_verified = self.is_verified

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.is_verified == True and self.__old_is_verified == False:
            xp_for_task = CampaignsTasks.objects.filter(
                campaign_task_id=self.campaign_task_id.campaign_task_id)[0].task_id.xp
            sum = self.user_id.current_xp + xp_for_task
            User.objects.filter(id=self.user_id.id).update(current_xp=sum)

        super().save(force_insert, force_update, *args, **kwargs)
        self.__old_is_verified = self.is_verified
