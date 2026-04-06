from flask import render_template, request
from flask.views import MethodView
import db_model

class Search(MethodView):
    def get(self):
        db = db_model.get_db()
        title = request.args.get('title', '').strip()
        author = request.args.get('author', '').strip()
        series = request.args.get('series', '').strip()

        author_first = author.split(' ')[0] if author else None
        author_last = author.split(' ')[-1] if author else None
        results = []
        if title and author:
            results = db.single_select(title=title, author_first=author_first or None, author_last=author_last or None)
        elif title:
            results = db.single_select(title=title)
        elif author:
            results = db.author_search(author_first=author_first, author_last=author_last)
        elif series:
            results = db.series_search(series=series)

        return render_template(
            'search.html',
            results=results,
            title_query=title,
            author_query=author,
            series_query=series
        )