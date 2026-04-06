#actual db structure using the model

import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from .Model import Model

load_dotenv()

class db(Model):
    def __init__(self):
        pass


    def check_dupe(self, title, author_first, author_last):
        """
        checks for a duplicate entry in the database before the insert
        return a boolean
        """
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor()
        sql = (
            'SELECT b.id from books as b '
            'JOIN book_authors as ba ON ba.book_id = b.id '
            'JOIN authors as a ON ba.author_id = a.id '
            'WHERE b.title = %(title)s '
            'AND a.author_first = %(author_first)s '
            'AND a.author_last = %(author_last)s '
        )
        params = {
            'title': title,
            'author_first': author_first,
            'author_last': author_last
        }
        try:
            cursor.execute(sql, params)
            return cursor.fetchone() is None
        except psycopg2.Error:
            print('Query Issue, contact admin')
        finally:
            cursor.close()
            connection.close()

    def recent_display(self):
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor()

        sql = (
            'SELECT b.title, b.date_added, '
            'a.author_first, a.author_last '
            'FROM books b '
            'JOIN book_authors ba ON b.id = ba.book_id '
            'JOIN authors a ON ba.author_id = a.id'
        )

        try:
            cursor.execute(sql + ' ORDER BY b.date_added DESC LIMIT 5')
            return cursor.fetchall()
        except psycopg2.Error:
            print('Query Issue, contact admin')
            return []
        finally:
            cursor.close()
            connection.close()

    def single_select(self, title=None, author_first=None, author_last=None):
        """Search the books table.

        Params are optional; when provided, they are matched using SQL LIKE.
        Returns a list of dicts: [{title, author, genre, publish_date, entry_date}, ...]
        """
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql = (
            'SELECT b.title, b.series, b.genre, b.first_pub, b.date_added, '
            'a.author_first, a.author_last '
            'FROM books b '
            'JOIN book_authors ba ON b.id = ba.book_id '
            'JOIN authors a ON ba.author_id = a.id'
        )
        conditions = []
        params = {}

        if title:
            conditions.append('b.title ILIKE %(title)s')
            params['title'] = f'%{title}%'
        if author_first or author_last:
            conditions.append(
                '(a.author_first ILIKE %(author_first)s OR a.author_last ILIKE %(author_last)s)'
            )
            params['author_first'] = f'%{author_first}%'
            params['author_last'] = f'%{author_last}%'

        if conditions:
            sql += ' WHERE ' + ' AND '.join(conditions)

        sql += ' ORDER BY b.date_added DESC'

        try:
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            connection.close()

    def author_search(self, author_first, author_last):
        """
        searches the database, finds and author
        if found, returns all books by that author

        PARAMS: author_first(string), author_last(string)
        RETURNS: list of dict objects containing book information
        """
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql = (
            'SELECT b.title, b.series, b.genre, b.version, b.first_pub, '
            'a.author_first, a.author_last '
            'FROM books b '
            'JOIN book_authors ba ON b.id = ba.book_id '
            'JOIN authors a ON a.id = ba.author_id '
            'WHERE a.author_first ILIKE %(author_first)s OR a.author_last ILIKE %(author_last)s'
        )
        params = {'author_first': f'%{author_first}%',
        'author_last': f'%{author_last}%'}

        try:
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            connection.close()

    def series_search(self, series):
        """
        searches the database, find a series and returns
        all books in the series

        PARAMS: series(string)
        RETURNS: list of dict objects with book information
        """

        connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql = (
            'SELECT b.title, b.series, b.version, b.first_pub, '
            'a.author_first, a.author_last '
            'FROM books b '
            'JOIN book_authors ba ON b.id = ba.book_id '
            'JOIN authors a ON a.id = ba.author_id '
            'WHERE b.series ILIKE %(series)s'
        )
        params = {'series': f'%{series}%'}

        try:
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            connection.close()

    def insert(self, title, author_first, author_last, series, genre, version, first_pub, publisher, date_added):
        """
        Insert a book into the books table.
        """

        if self.check_dupe(title, author_first, author_last):
            books_params = {
                'title': title,
                'series': series,
                'genre': genre,
                'first_pub': first_pub,
                'version': version,
                'publisher': publisher,
                'date_added': date_added,
            }

            author_params = {
                'author_first': author_first,
                'author_last': author_last
            }

            connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
            cursor = connection.cursor()
            try:
                cursor.execute(
                    'INSERT INTO books (title, series, genre, first_pub, version, publisher, date_added) '
                    'VALUES (%(title)s, %(series)s, %(genre)s, %(first_pub)s, %(version)s, %(publisher)s, %(date_added)s) RETURNING id',
                    books_params,
                )
                book_id = cursor.fetchone()[0]
                cursor.execute(
                    'INSERT INTO authors (author_first, author_last) '
                    'VALUES (%(author_first)s, %(author_last)s) '
                    'ON CONFLICT ON CONSTRAINT "unique author" '
                    'DO UPDATE SET author_first = EXCLUDED.author_first '
                    'RETURNING id',
                    author_params,
                )
                author_id = cursor.fetchone()[0]

                cursor.execute(
                    'INSERT INTO book_authors (book_id, author_id) '
                    'VALUES (%(book_id)s, %(author_id)s)',
                    {'book_id': book_id, 'author_id': author_id},
                )
                connection.commit()
                
                return True
            finally:
                cursor.close()
                connection.close()

    def delete_book(self, title):
        """
        Delete a book from the books table by title.
        """

        #look into deleting authors with no books as part of the deletion processes
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor()
        try:
            cursor.execute(
                'DELETE FROM book_authors WHERE book_id = (SELECT id FROM books WHERE title ILIKE %s)',
                (title,)
            )
            cursor.execute('DELETE FROM books WHERE title ILIKE %s', (title,))
            connection.commit()
        except psycopg2.Error:
            connection.rollback()
            print('Delete failed, contact admin')
        finally:
            cursor.close()
            connection.close()