from django.contrib import admin

# Register your models here.
from .models import Campaign, UsersTasks, Tasks, CampaignsTasks

admin.site.register(Campaign)
admin.site.register(UsersTasks)
admin.site.register(Tasks)
admin.site.register(CampaignsTasks)
