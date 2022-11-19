from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
        except:
            return Response({
                'error': 'User doesn\'t exists'
            }, status=401)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({
                'message': 'Wrong username or password'
            }, status=401)

        login(request, user)

        return Response({
            'message': 'Logged in'
        }, status=200)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        # TODO: chekc if user exists
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return Response({
                'message': 'User has been registered'
            }, status=200)

        return Response({
            'message': 'Could not register new user',
            'reason': [error for form_input in form.errors for error in form.errors[form_input]]
        }, status=401)


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)

        return Response({}, status=200)


class IsLoggedInView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_user(request)

        if user.is_active:
            return Response({
                'message': 'User is logged in'
            }, status=200)

        return Response({
            'message': 'User is not logged in'
        }, status=404)
