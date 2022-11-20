from authentication.user.serializers import UserRegistrationSerializer, UserLoginSerializer

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from django.contrib.auth import logout


class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            response = {
                'message': str(e),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response = {
            'message': 'User registered successfully',
            'token': serializer.data['token']
        }

        return Response(response, status=status.HTTP_201_CREATED)


class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            response = {
                'message': str(e),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'message': 'User logged in successfully',
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)
