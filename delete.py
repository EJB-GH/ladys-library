from flask import render_template, request, redirect, url_for
from flask.views import MethodView
import db_model

class Delete(MethodView):
    def get(self):
        return render_template('delete.html')

    def post(self):
        db = db_model.get_db()
        title = request.form.get('title', '').strip()

        db.delete_book(title)

        #possibly run check on book_authors table to see if no key present after deletion, if so
        #delete author as well, as no books are present in the list
        
        return redirect(url_for('index'))