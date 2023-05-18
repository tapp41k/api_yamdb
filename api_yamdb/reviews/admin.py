from django.contrib import admin
# Из модуля models импортируем модель Post
from .models import Categories, Title, Genres, GenreTitle

admin.site.register(Categories)
admin.site.register(Title)
admin.site.register(Genres)
admin.site.register(GenreTitle)
