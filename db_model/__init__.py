from .db import db

appmodel = db()

def get_db():
    return appmodel