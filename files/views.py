import os
from rest_framework.views import APIView
from . import drive
from rest_framework.parsers import FileUploadParser
import tempfile
from rest_framework.response import Response
from rest_framework import status


class UploadFileView(APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request, format='txt'):
        up_file = request.FILES['file']
        with CustomNamedTemporaryFile(mode='wb+') as tmp:
            for chunk in up_file.chunks():
                tmp.write(chunk)
            tmp.write(chunk)

            textfile = drive.CreateFile()
            textfile.SetContentFile(os.path.basename(str(up_file)))
            textfile.Upload()

            drive.CreateFile(
                {'id': textfile['id']}).GetContentFile(os.path.basename(str(up_file)))
        return Response({}, status=status.HTTP_201_CREATED)

# class DownloadFileView(RetrieveAPIView):
#     ...


class CustomNamedTemporaryFile:
    """
    This custom implementation is needed because of the following limitation of tempfile.NamedTemporaryFile:

    > Whether the name can be used to open the file a second time, while the named temporary file is still open,
    > varies across platforms (it can be so used on Unix; it cannot on Windows NT or later).
    """

    def __init__(self, mode='wb', delete=False):
        self._mode = mode
        self._delete = delete

    def __enter__(self):
        # Generate a random temporary file name
        file_name = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        # Ensure the file is created
        # Open the file in the given mode
        self._tempFile = open(file_name, self._mode)
        return self._tempFile

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tempFile.close()
        if self._delete:
            os.remove(self._tempFile.name)
