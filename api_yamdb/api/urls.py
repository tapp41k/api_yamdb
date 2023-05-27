from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet, GenreViewSet, CategoriesViewSet,
                    ReviewViewSet,
                    CommentViewSet)
from users.views import APISignupView, APITokenView, UsersViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
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
