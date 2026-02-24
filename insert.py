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
        author = request.form.get('author', '').strip()
        genre = request.form.get('genre', '').strip()
        publish_date = request.form.get('publish_date', '').strip()
        entry_date = str(date.today())

        db.insert(title, author, genre, publish_date, entry_date)
        return redirect(url_for('index'))