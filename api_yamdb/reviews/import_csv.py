import csv
import sqlite3

path_for_db = 'api_yamdb/db.sqlite3'
dir_csv = 'api_yamdb/static/data/'
name_file_category = 'category.csv'
name_file_comments = 'comments.csv'
name_file_genre_title = 'genre_title.csv'
name_file_genre = 'genre.csv'
name_file_review = 'review.csv'
name_file_titles = 'titles.csv'
name_file_users = 'users.csv'


# id,name,slug
def import_category():
    con = sqlite3.connect(path_for_db)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE reviews_category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            slug TEXT)""")
    except sqlite3.OperationalError as error:
        print(f'таблица Категория уже существует, новую не создаем: {error}')
    finally:
        with open(dir_csv + name_file_category, 'r', encoding="utf8") as f:
            dr = csv.DictReader(f, delimiter=",")
            to_db = [(i['id'], i['name'], i['slug']) for i in dr]

        cur.executemany(
            "INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);",
            to_db)
        con.commit()
        con.close()


# id,name,slug
def import_genre():
    con = sqlite3.connect(path_for_db)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE reviews_genre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            slug TEXT)""")
    except sqlite3.OperationalError as error:
        print(f'таблица Жанры уже существует, новую не создаем: {error}')
    finally:
        with open(dir_csv + name_file_genre, 'r', encoding="utf8") as f:
            dr = csv.DictReader(f, delimiter=",")
            to_db = [(i['id'], i['name'], i['slug']) for i in dr]

        cur.executemany(
            "INSERT INTO reviews_genre (id, name, slug) VALUES (?, ?, ?);",
            to_db)
        con.commit()
        con.close()


# id,review_id,text,author,pub_date
def import_comments():
    con = sqlite3.connect(path_for_db)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE reviews_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id INTEGER,
            text TEXT,
            author TEXT,
            pub_date TEXT)""")
    except sqlite3.OperationalError as error:
        print(f'таблица Комментарии уже существует, новую не создаем: {error}')
    finally:
        with open(dir_csv + name_file_comments, 'r', encoding="utf8") as f:
            dr = csv.DictReader(f, delimiter=",")
            to_db = [
                (i['id'],
                 i['review_id'],
                 i['text'],
                 i['author'],
                 i['pub_date']) for i in dr]

        cur.executemany(
            "INSERT INTO reviews_comments "
            "(id, review_id, text, author, pub_date)"
            "VALUES (?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        con.close()


# id,title_id,genre_id
def import_genre_title():
    con = sqlite3.connect(path_for_db)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE reviews_genretitle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_id INTEGER,
            genre_id INTEGER)""")
    except sqlite3.OperationalError as error:
        print(f'таблица Жанры-Названия существует, новую не создаем: {error}')
    finally:
        with open(dir_csv + name_file_genre_title, 'r', encoding="utf8") as f:
            dr = csv.DictReader(f, delimiter=",")
            to_db = [(i['id'], i['title_id'], i['genre_id']) for i in dr]

        cur.executemany(
            "INSERT INTO reviews_genretitle (id, title_id, genre_id) "
            "VALUES (?, ?, ?);",
            to_db)
        con.commit()
        con.close()


# id,title_id,text,author,score,pub_date
def import_review():
    con = sqlite3.connect(path_for_db)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE reviews_review (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_id INTEGER,
            text TEXT,
            author TEXT,
            score INTEGER,
            pub_date TEXT)""")
    except sqlite3.OperationalError as error:
        print(f'таблица Ревью уже существует, новую не создаем: {error}')
    finally:
        with open(dir_csv + name_file_review, 'r', encoding="utf8") as f:
            dr = csv.DictReader(f, delimiter=",")
            to_db = [
                (i['id'],
                 i['title_id'],
                 i['text'],
                 i['author'],
                 i['score'],
                 i['pub_date']) for i in dr]

        cur.executemany(
            "INSERT INTO reviews_review "
            "(id, title_id, text, author, score, pub_date) "
            "VALUES (?, ?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        con.close()


# id,name,year,category
def import_titles():
    con = sqlite3.connect(path_for_db)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE reviews_title (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            year INTEGER,
            category_id INTEGER)""")
    except sqlite3.OperationalError as error:
        print(f'таблица Названия уже существует, новую не создаем: {error}')
    finally:
        with open(dir_csv + name_file_titles, 'r', encoding="utf8") as f:
            dr = csv.DictReader(f, delimiter=",")
            to_db = [
                (i['id'],
                 i['name'],
                 i['year'],
                 i['category']) for i in dr]

        cur.executemany(
            "INSERT INTO reviews_title (id, name, year, category_id) "
            "VALUES (?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        con.close()


# id,username,email,role,bio,first_name,last_name
def import_users():
    con = sqlite3.connect(path_for_db)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE reviews_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            role TEXT,
            bio TEXT,
            first_name TEXT,
            last_name TEXT)""")
    except sqlite3.OperationalError as error:
        print(f'таблица Пользователь существует, новую не создаем: {error}')
    finally:
        with open(dir_csv + name_file_users, 'r', encoding="utf8") as f:
            dr = csv.DictReader(f, delimiter=",")
            to_db = [
                (i['id'],
                 i['username'],
                 i['email'],
                 i['role'],
                 i['bio'],
                 i['first_name'],
                 i['last_name']) for i in dr]

        cur.executemany(
            "INSERT INTO reviews_users "
            "(id, username, email, role, bio, first_name, last_name) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        con.close()


import_category()
import_genre()
import_titles()
import_genre_title()

import_comments()
import_review()
import_users()
