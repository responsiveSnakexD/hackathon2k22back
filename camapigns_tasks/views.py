from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from camapigns_tasks.models import CampaignsTasks, Tasks
# Create your views here.


class TaskView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('task_id')
        task = Tasks.objects.filter(task_id=id)[0]
        response = {
            'task_id': task.task_id,
            'title': task.title,
            'description': task.description,
            'goal': task.goal,
            'documentation': task.documentation,
            'xp': task.xp,
        }

        return Response(response, status=status.HTTP_201_CREATED)


class TasksView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('campaign_id')
        campaign_task = CampaignsTasks.objects.filter(campaign_id=id)
        response = {}
        for task in campaign_task:
            response[task.task_id.task_id] = task.task_id.title

        return Response(response, status=status.HTTP_201_CREATED)
