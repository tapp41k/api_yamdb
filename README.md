# Проект YaMDb - сервис отзывов на произведения

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Технологии:
- Python 3.9
- Django 3.2
- Django REST framework 3.12.4
- библиотека Simple JWT - работа с JWT-токеном

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tapp41k/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

- Для Windows
```
python -m venv venv
```
```
source venv/Scripts/activate
```

- Для Linux, MacOS
```
python3 -m venv venv
```
```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Обновить pip

- Для Windows
```
python -m pip install --upgrade pip
```

- Для Linux, MacOS
```
python3 -m pip install --upgrade pip
```

Создать миграции:

- Для Windows
```
python manage.py makemigrations
```
- Для Linux, MacOS
```
python3 manage.py makemigrations
```

Выполнить миграции:

- Для Windows
```
python manage.py migrate
```

- Для Linux, MacOS
```
python3 manage.py migrate
```

Запустить проект:

- Для Windows
```
python manage.py runserver
```

- Для Linux, MacOS
```
python3 manage.py runserver
```

## Документация к запросам

С документацией к запросам можно ознакомиться по адресу

```
http://127.0.0.1:8000/redoc/
```

## Команда разработки
[Илья Осадчий](https://github.com/tapp41k) - управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail.

[Анна Митрофанова](https://github.com/Ann-mitr) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них.

[Павел Войнов](https://github.com/R1su) - отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений.
