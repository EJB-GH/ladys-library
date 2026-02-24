from flask import render_template
from flask.views import MethodView
import db_model


class Index(MethodView):
    def get(self):
        db = db_model.get_db()
        entries = [
            dict(title=row[0], author=row[1], entry_date=row[2])
            for row in db.recent_display()
        ]
        return render_template("index.html", entries=entries)
