from django.urls import include, path

from .views import LoginApiView, SignUpView, ProfileApiView
urlpatterns = [
    path(
        'signup',
        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'login',
        LoginApiView.as_view(),
        name='login'
    ),
    path(
        'profile',
        ProfileApiView.as_view(),
        name='profile'
    ),
]