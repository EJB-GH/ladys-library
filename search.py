from flask import render_template, request
from flask.views import MethodView
import db_model

class Search(MethodView):
    def get(self):
        db = db_model.get_db()
        title = request.args.get('title', '').strip()
        author = request.args.get('author', '').strip()

        author_first = author.split(' ')[0] if author else None
        author_last = author.split(' ')[-1] if author else None
        results = []
        if title or author:
            results = db.single_select(title=title or None, author_first=author_first or None, author_last=author_last or None)

        return render_template(
            'search.html',
            results=results,
            title_query=title,
            author_query=author,
        )