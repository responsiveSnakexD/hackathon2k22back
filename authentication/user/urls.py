from django.urls import path
from authentication.user.views import UserRegistrationView, UserLoginView


urlpatterns = [
    path(r'signup', UserRegistrationView.as_view()),
    path(r'signin', UserLoginView.as_view()),
    #path(r'signout', UserSignOutView.as_view())
]
