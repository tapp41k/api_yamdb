from rest_framework import viewsets, permissions


from reviews.models import Title, Genres, Categories
from .permission import IsAdminOrReadOnly
from .serializers import (TitleSerializer,
                          GenresSerializer,
                          CategoriesSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

    permission_classes = [IsAdminOrReadOnly]


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.AllowAny]

    permission_classes = [IsAdminOrReadOnly]
