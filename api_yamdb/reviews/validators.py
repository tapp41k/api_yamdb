from django.core.exceptions import ValidationError
import datetime


def validate_year(value):
    # Проверка год больше текущего
    year_now = datetime.datetime.now().year
    if value > year_now:
        raise ValidationError(
            'Год издания не может быть больше текущего года',
            params={'value': value},
        )
