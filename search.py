from flask import render_template, request
from flask.views import MethodView
import db_model

class Search(MethodView):
    def get(self):
        db = db_model.get_db()
        title = request.args.get('title', '').strip()
        author = request.args.get('author', '').strip().rsplit(' ', 1)
        author_first = author[0] if len(author) > 0 else '' 
        author_last = author[1] if len(author) > 1 else ''


        results = []
        if title or author:
            results = db.single_select(title=title or None, author_f=author_first or None, author_l=author_last or None)
           

        return render_template(
            'search.html',
            results=results,
            title_query=title,
            author_query=f"{author_first} {author_last}",
        )