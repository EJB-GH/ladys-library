from flask import render_template, request, redirect, url_for
from flask.views import MethodView
import db_model
from datetime import date

class Insert(MethodView):
    def get(self):
        return render_template('insert.html')

    def post(self):

        #capitalize first letter of each word in book titles
        #same with author, pub, etc.
        db = db_model.get_db()

        title = request.form.get('title', '').strip()
        author_parts = request.form.get('author', '').strip().rsplit(' ', 1)
        author_first = author_parts[0]
        author_last = author_parts[1] if len(author_parts) > 1 else ''
        series = request.form.get('series', '').strip()
        genre = request.form.get('genre', '').strip()
        version = request.form.get('version', '').strip()
        first_pub = request.form.get('publish_date', '').strip()
        publisher = request.form.get('publisher', '').strip()
        date_added = str(date.today())

        db.insert(title, author_first, author_last, series, genre, version, first_pub, publisher, date_added)
        return redirect(url_for('index'))