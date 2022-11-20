from django.urls import path
from files.views import UploadFileView

urlpatterns = [
    path('upload', UploadFileView.as_view()),
    #path('download', )
]
