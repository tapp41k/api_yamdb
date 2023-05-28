import csv
import os

from django.core.management import BaseCommand
from django.db import IntegrityError
from api_yamdb.settings import FILES_DB_DIR
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
)
from users.models import User


files_for_models = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review,
    'comments': Comment,
}

fields_for_models = {
    'category': ('category', Category),
    'genre_id': ('genre', Genre),
    'title_id': ('title', Title),
    'author': ('author', User),
    'review_id': ('review', Review),
}


def open_file(file_name):
    csv_path = os.path.join(FILES_DB_DIR, file_name + '.csv')
    try:
        with (open(csv_path, encoding='utf-8')) as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        raise FileNotFoundError((f'Файл {file_name}.csv не найден.'))


def add_values(data_csv):
    data_for_add = data_csv.copy()
    for field, value in data_csv.items():
        if field in fields_for_models.keys():
            field0 = fields_for_models[field][0]
            data_for_add[field0] = fields_for_models[field][1].objects.get(
                pk=value)
    return data_for_add


def load_csv(file_name, class_name, data):
    rows = data[1:]
    if not (rows):
        raise Exception(f'БД {file_name}.csv нет данных для загрузки')
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = add_values(data_csv)
        try:
            table = class_name(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            raise Exception(f'Ошибка в загружаемых данных. {error}. '
                            f'Попытка загрузить БД {file_name}.csv '
                            f'в таблицу {class_name.__qualname__} провалена.')
    return (f'БД {file_name}.csv успешно загружена '
            f'в таблицу {class_name.__qualname__}.')


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('ПРОЦЕСС ИМПОРТА ЗАПУЩЕН.'))
        for key, value in files_for_models.items():
            print(f'Импорт БД в таблицу {value.__qualname__}')
            try:
                data = open_file(key)
                if not (data):
                    raise Exception(f'БД {key}.csv пуста')
                try:
                    import_csv = load_csv(key, value, data)
                    self.stdout.write(self.style.SUCCESS(import_csv))
                except Exception as error:
                    self.stdout.write(self.style.WARNING(error))
            except Exception as error:
                self.stdout.write(self.style.WARNING(error))
        self.stdout.write(self.style.SUCCESS('ПРОЦЕСС ИМПОРТА ЗАВЕРШЕН.'))
