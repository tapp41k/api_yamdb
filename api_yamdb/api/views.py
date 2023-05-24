from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, pagination
from reviews.models import Review, Comment, Category, Genre, Title

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .permission import IsAdminOrReadOnly
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitleSerializer,
                          TitleSerializerForCreate,
                          ReviwSerializer,
                          CommentSerializer,
                          TitleSerializerForRetrieve)

from .mixins import CreateListDestroyViewSet


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return TitleSerializerForCreate
        if self.action == 'retrieve':
            return TitleSerializerForRetrieve
        return TitleSerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = ReviwSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title().id)

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_class = (IsAuthenticatedOrReadOnly)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review().id)

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, review=self.get_review()
        )
