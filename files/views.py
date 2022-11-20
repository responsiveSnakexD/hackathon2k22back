import os
import uuid
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
import tempfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from camapigns_tasks.models import CampaignsTasks, UsersTasks, User
from pathlib import Path

home = str(Path.home())


class UploadFileView(APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request: Request, format='jpg', *args, **kwargs):
        campaign_id = kwargs.get('campaign_id')
        task_id = kwargs.get('task_id')
        up_file = request.FILES['file']
        filename = os.path.join(home, str(uuid.uuid4()).replace('-', ''))

        token = request.META.get("HTTP_AUTHORIZATION")
        print(request.META)
        user_id = User.objects.filter(token=token)[0].id

        campaign_task_id = CampaignsTasks.objects.filter(
            task_id=task_id, campaign_id=campaign_id)[0].campaign_task_id

        with up_file.open(mode='rb') as f1:
            with open(file=filename, mode="wb+") as f2:
                # adjust the chunk size as desired
                while contents := f1.file.read(1024 * 1024):
                    f2.write(contents)
        UsersTasks.objects.filter(
            campaign_task_id=campaign_task_id, user_id=user_id).update(url=os.path.basename(filename))

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class DownloadFileView(APIView):
    parser_classes = (FileUploadParser, )

    def put(self, request: Request, *args, **kwargs):
        campaign_id = kwargs.get('campaign_id')
        task_id = kwargs.get('task_id')
        up_file = request.FILES['file']
        filename = os.path.join(home, str(uuid.uuid4()).replace('-', ''))

        token = request.META.get("HTTP_AUTHORIZATION")
        user_id = User.objects.filter(token=token)[0].id

        campaign_task_id = CampaignsTasks.objects.filter(
            task_id=task_id, campaign_id=campaign_id)[0].campaign_task_id

        with up_file.open(mode='rb') as f1:
            with open(file=filename, mode="wb+") as f2:
                # adjust the chunk size as desired
                while contents := f1.file.read(1024 * 1024):
                    f2.write(contents)
        UsersTasks.objects.filter(
            campaign_task_id=campaign_task_id, user_id=user_id).update(url=os.path.basename(filename))

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CustomNamedTemporaryFile:
    """
    This custom implementation is needed because of the following limitation of tempfile.NamedTemporaryFile:

    > Whether the name can be used to open the file a second time, while the named temporary file is still open,
    > varies across platforms (it can be so used on Unix; it cannot on Windows NT or later).
    """

    def __init__(self, mode='wb', delete=False, format=""):
        self._mode = mode
        self._delete = delete
        self._format = format

    def __enter__(self):
        # Generate a random temporary file name
        file_name = os.path.join(
            tempfile.gettempdir(), os.urandom(24).hex() + "." + self._format)
        # Ensure the file is created
        # Open the file in the given mode
        self._tempFile = open(file_name, self._mode)
        return self._tempFile

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tempFile.close()
        if self._delete:
            os.remove(self._tempFile.name)
