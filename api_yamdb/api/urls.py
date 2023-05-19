from django.urls import path

from users.views import APITokenView, APISignupView

urlpatterns = [
    path(
        'v1/auth/token/',
        APITokenView.as_view(),
        name='get_token'
    ),
    path(
        'v1/auth/signup/',
        APISignupView.as_view(),
        name='signup'
    ),
]
