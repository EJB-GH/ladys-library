#actual db structure using the model

import os
import sqlite3
import psycopg2
from dotenv import load_dotenv
from .Model import Model
from datetime import date

load_dotenv()

db_file = 'library.db'

def ret_con():
    '''
    simple send connection function to save space
    in class functions
    RETURNS: a connection to the db
    '''
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    return connection, cursor

class db(Model):
    def __init__(self):

        #initial connection if the db exists, else make it
        connection, cursor = ret_con()

        #execute a select to test db existence
        try:
            cursor.execute('select * from books')
        except sqlite3.OperationalError:
            cursor.execute('create table books (title, author, genre, publish_date, entry_date)')

        connection.commit()

        cursor.close()
        connection.close()

    def recent_display(self):
        connection, cursor = ret_con()

        try:
            cursor.execute('select title, author, entry_date from books order by entry_date desc limit 5')
            return cursor.fetchall()
        except sqlite3.OperationalError:
            print('Query Issue, contact admin')
            return []
        finally:
            cursor.close()
            connection.close()

    def single_select(self, title=None, author=None):
        """Search the books table.

        Params are optional; when provided, they are matched using SQL LIKE.
        Returns a list of dicts: [{title, author, genre, publish_date, entry_date}, ...]
        """
        connection = sqlite3.connect(db_file)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        sql = 'select title, author, genre, publish_date, entry_date from books'
        conditions = []
        params = {}

        if title:
            conditions.append('title like :title')
            params['title'] = f'%{title}%'
        if author:
            conditions.append('author like :author')
            params['author'] = f'%{author}%'

        if conditions:
            sql += ' where ' + ' and '.join(conditions)

        sql += ' order by entry_date desc'

        try:
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            connection.close()

    def insert(self, title, series, genre, first_pub, ver_edition, author_first, author_last, pub_name):
        """
        Insert a book into the books table.
        """
        params = {
            'title': title,
            'series': series,
            'genre': genre,
            'first_pub': first_pub,
            'ver_edition': ver_edition,
            'author_first': author_first,
            'author_last': author_last,
            'pub_name': pub_name,
            'date_added': date.today(),
        }

        connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor()
        try:
            cursor.execute(
                'INSERT INTO books (title, series, genre, first_pub, ver_edition, author_first, author_last, pub_name, date_added) '
                'VALUES (%(title)s, %(series)s, %(genre)s, %(first_pub)s, %(ver_edition)s, %(author_first)s, %(author_last)s, %(pub_name)s, %(date_added)s)',
                params,
            )
            connection.commit()
            return True
        finally:
            cursor.close()
            connection.close()