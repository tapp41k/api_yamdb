from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Comment
from .serializers import ReviwSerializer, CommentSerializer


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
