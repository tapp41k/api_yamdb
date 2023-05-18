from rest_framework import serializers

from reviews.models import Title, Genres, Categories


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'
