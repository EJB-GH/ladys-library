'''
Main driver file for library application
'''
import flask
from index import Index

app = flask.Flask(__name__, template_folder="template")

app.add_url_rule("/", view_func=Index.as_view("index"))

if __name__ == '__main__':
    app.run(debug=True)
