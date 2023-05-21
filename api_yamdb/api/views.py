from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, pagination
from reviews.models import Category, Genre, Title

from .permission import IsAdminOrReadOnly
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitleSerializer,
                          TitleSerializerForCreate)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')

    def perform_create(self):
        return TitleSerializerForCreate


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
