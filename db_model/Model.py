#the outline for the model used for the database

class Model():
    def single_select(self, title=None, author_first=None, author_last=None):
        """
        INPUT: title(str|None), author_first(str|None), author_last(str|None)
        Search the datastore and return matching books.
        """
        pass

    def author_search(self, author_first, author_last):
        pass

    def series_search(self, series):
        pass

    def insert(self, title, author_first, author_last, series, genre, version, first_pub, publisher, date_added):
        pass

    def delete_book(self, title):
        pass


