from flask import render_template, request
from flask.views import MethodView
import db_model

class Search(MethodView):
    def get(self):
        db = db_model.get_db()
        title = request.args.get('title', '').strip()
        author = request.args.get('author', '').strip()

        results = []
        if title or author:
            results = db.single_select(title=title or None, author=author or None)
           

        return render_template(
            'search.html',
            results=results,
            title_query=title,
            author_query=author,
        )