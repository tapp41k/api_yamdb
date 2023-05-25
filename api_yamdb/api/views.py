from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, pagination
from reviews.models import Review, Comment, Category, Genre, Title

from rest_framework.pagination import PageNumberPagination
from .permission import IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitleSerializer,
                          TitleSerializerForCreate,
                          ReviwSerializer,
                          CommentSerializer)

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        Avg("reviews_title__score")
    )
    serializer_class = TitleSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleSerializerForCreate
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
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title().id)

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_review(self):
        pk = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=pk)
        return review

    def get_title(self):
        pk = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        return title

    def get_queryset(self):
        return Comment.objects.filter(
            review__title=self.get_title(),
            review=self.get_review()
        ).select_related('author', 'review')

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)
