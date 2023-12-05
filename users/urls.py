from django.urls import path
from . views import *

BASE_URL = 'auth'

urlpatterns = [
    path(BASE_URL + '/register', SignUpUserView.as_view() , name='signup'),
    path(BASE_URL + '/login', SignInUserView.as_view() , name="login"), 
    path(BASE_URL + '/logout', LogOutView.as_view(), name="logout"),
    path(BASE_URL + '/logout_all_devices' , LogoutAllDevicesView.as_view(), name="logout all"),
    path('users/' , GetUsersView.as_view() , name='filter users'),
    path('users/' , UpdateUserProfileView.as_view() , name='rest password'),
    path(BASE_URL + '/password_reset_request' , ValidationCodesView.as_view() , name="gen validation code"),
    path(BASE_URL + '/password_reset_request' , VerifyValidationCode.as_view() , name="verify pass code "),
    path(BASE_URL + '/password_reset' , PassWordResetView.as_view() , name="reset pass code "),
    # path(route='mail', view=RequestPasswordReset.as_view() , name='send_mail'),
    path(route='mail', view=mailer , name='send_mail'),
]