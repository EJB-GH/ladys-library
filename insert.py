from flask import render_template, request, redirect, url_for
from flask.views import MethodView
import db_model
from datetime import date

class Insert(MethodView):
    def get(self):
        return render_template('insert.html')

    def post(self):
        db = db_model.get_db()

        title = request.form.get('title', '').strip()
        author_first = request.form.get('author_first', '').strip()
        author_last = request.form.get('author_last', '').strip()
        series = request.form.get('series', '').strip()
        genre = request.form.get('genre', '').strip()
        version = request.form.get('version', '').strip()
        publish_date = request.form.get('publish_date', '').strip()
        publisher = request.form.get('publisher', '').strip()
        entry_date = str(date.today())

        db.insert(title, author_first, author_last, series, genre, version, publish_date, publisher, entry_date)
        return redirect(url_for('index'))