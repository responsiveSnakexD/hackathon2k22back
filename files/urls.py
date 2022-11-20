from django.urls import path
from files.views import UploadFileView, DownloadFileView

urlpatterns = [
    path('upload/<int:campaign_id>/<int:task_id>', UploadFileView.as_view()),
    path('download/<string:url>', DownloadFileView.as_new())
]
