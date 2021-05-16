from django.test import TestCase
from google_api.google_api import GoogleBookApiWrapper


class GoogleApiWrapper(TestCase):
    TEST_BOOK_TITLE = 'Lion King'

    def test_search_books(self):
        self.assertTrue(GoogleBookApiWrapper().get_book_by_title(self.TEST_BOOK_TITLE))

    def test_search_result_books(self):
        list_keys = ['title', 'author', 'publisher', 'publishedDate', 'pageCount', 'description']
        book_data = GoogleBookApiWrapper().get_book_by_title(self.TEST_BOOK_TITLE)
        for key in list_keys:
            if key not in book_data:
                self.assertTrue(False)
        self.assertTrue(True)
