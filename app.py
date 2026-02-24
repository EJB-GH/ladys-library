'''
Main driver file for library application
'''
import flask
from index import Index
from search import Search
from insert import Insert

app = flask.Flask(__name__, template_folder="template")

app.add_url_rule("/", view_func=Index.as_view("index"))
app.add_url_rule("/search", view_func=Search.as_view("search"))
app.add_url_rule("/insert", view_func=Insert.as_view("insert"), methods=['GET', 'POST'])
if __name__ == '__main__':
    app.run(debug=True)
