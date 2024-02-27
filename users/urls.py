from django.urls import path
from . views import *
from rest_framework.routers import DefaultRouter

BASE_URL = 'auth'

router = DefaultRouter()
router.register('roles', GroupView, 'role')
router.register('permissions', PermissionView, 'permission')

urlpatterns = [
    path(BASE_URL + '/register', SignUpUserView.as_view(), name='signup'),
    path(BASE_URL + '/login', SignInUserView.as_view(), name="login"),
    path(BASE_URL + '/logout', LogOutView.as_view(), name="logout"),
    path(BASE_URL + '/logout_all_devices',
         LogoutAllDevicesView.as_view(), name="logout all"),
    path('users/', GetUsersView.as_view(), name='filter users'),
    path('user/profile/<str:pk>', UpdateUserProfileView.as_view(), name='update user view'),
    path(BASE_URL + '/password_reset_request',
         ValidationCodesView.as_view(), name="gen validation code"),
    path(BASE_URL + '/password_reset_request',
         VerifyValidationCode.as_view(), name="verify pass code "),
    path(BASE_URL + '/change-password/',
         ChangePasswordView.as_view(), name='change-password'),
    path(route='mail', view=mailer, name='send_mail'),
    path(route='welcome/', view=HomeScreenDataView.as_view(), name='home data'),
]
urlpatterns += router.urls
