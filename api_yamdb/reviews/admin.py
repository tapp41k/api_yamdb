from django.contrib import admin

from .models import Category, Title, Genre, GenreTitle

admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(GenreTitle)
