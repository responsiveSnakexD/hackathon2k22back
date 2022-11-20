from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from camapigns_tasks.models import CampaignsTasks, Tasks, Campaign
from datetime import datetime
# Create your views here.

class TaskView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('task_id')
        task = Tasks.objects.filter(task_id = id)[0]
        response = {
            'task_id': task.task_id,
            'title': task.title,
            'description': task.description,
            'goal': task.goal,
            'documentation': task.documentation,
            'xp': task.xp
        }

        return Response(response, status=status.HTTP_201_CREATED)

class TasksView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('campaign_id')
        campaign_task = CampaignsTasks.objects.filter(campaign_id = id)
        response = {}
        for task in campaign_task:
            response[task.task_id.task_id] = task.task_id.title
        

        return Response(response, status=status.HTTP_201_CREATED)
    

# endpoint do danych kampanii (nazwa, opis, id kampani, tylko aktualnej kampani)
class CampaignView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        for campaign in Campaign.objects.all():
            start_date = campaign.start_date
            end_date = campaign.end_date
            today = datetime.today().now().date()
            if start_date <= today and end_date >= today:
                response = {
                    "camapign_id": campaign.camapign_id,
                    "title": campaign.title,
                    # "description": campaign.description
                }
                return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'message': 'No campaign is happening'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # campaign = Campaign.objects.filter()[0]
        # print(campaign)
        # response = {}
        # for task in campaign_task:
        #     response[task.task_id.task_id] = task.task_id.title
        

        # 

