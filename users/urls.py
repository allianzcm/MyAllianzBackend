from django.urls import path, include
from . views import *
from knox.views import LogoutAllView

urlpatterns = [
    path('register', SignUpAPI.as_view() , name='signup'),
    path('login', SignInAPI.as_view() , name="login"), 
    path('logout',Logout.as_view(), name="logout"),
    path('logout/all',LogoutAllView.as_view(), name="logout_all"),
    path('password/reset', password_reset , name='rest_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]