"""hackathon2k22back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#from authentication.views import LoginView, RegisterView, LogoutView, IsLoggedInView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),


    path('api/auth/', include('authentication.user.urls')),
    path('api/task/', include('camapigns_tasks.urls')),
    path('api/files/', include('files.urls'))
    #path('auth', include('authentication.user.urls'))
    # path('auth/register/', RegisterView.as_view(), name="RegisterView"),
    # path('auth/login/', LoginView.as_view(), name="LoginView"),
    # path('auth/logout/', LogoutView.as_view(), name="LogoutView"),
    # path('auth/is-logged-in/', IsLoggedInView.as_view(), name="IsLoggedInView")
]
