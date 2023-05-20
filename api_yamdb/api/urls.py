from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoriesViewSet

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]
