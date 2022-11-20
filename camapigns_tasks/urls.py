from django.urls import path
from camapigns_tasks.views import TaskView, TasksView, CampaignView


urlpatterns = [
    path('all/<int:campaign_id>', TasksView.as_view()),
    path('<int:task_id>', TaskView.as_view()),
    path('campaign', CampaignView.as_view()),
]

# api/task/task_id/campain_id
