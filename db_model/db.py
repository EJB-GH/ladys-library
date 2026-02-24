#actual db structure using the model

import sqlite3
from .Model import Model
from datetime import date

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

    def insert(self, title, author, genre, publish_date, entry_date):
        """
        Insert a book into the books table.
        """
        params = {
            'title': title,
            'author': author,
            'genre': genre,
            'publish_date': publish_date,
            'entry_date': entry_date,
        }

        connection, cursor = ret_con()
        try:
            cursor.execute(
                'insert into books (title, author, genre, publish_date, entry_date) '
                'values (:title, :author, :genre, :publish_date, :entry_date)',
                params,
            )
            connection.commit()
            return True
        finally:
            cursor.close()
            connection.close()