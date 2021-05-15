import json
import requests
import environ


class GoogleBookApiWrapper:
    URL_PATTERNS = {'searching_url': 'https://www.googleapis.com/books/v1/'
                                     'volumes?q={0}&key={1}&maxResults={2}'}
    MAX_RESPONSES_NUMBER = 5

    def __init__(self):
        ENV = environ.Env()
        environ.Env.read_env()
        self.API_KEY = ENV('GOOGLE_API_KEY')

    def get_book_by_title(self, book_title):
        response = requests.get(
            url=GoogleBookApiWrapper.URL_PATTERNS['searching_url'].format(
                book_title, self.API_KEY, self.MAX_RESPONSES_NUMBER))
        return self.parse_data(response.content)

    def parse_data(self, book_data):
        book_data = json.loads(book_data)
        all_books = []
        for item in book_data['items']:
            volume_info = item['volumeInfo']
            data = {'title': volume_info.get('title'),
                    'author': volume_info.get('authors'),
                    'publisher': volume_info.get(
                        'publisher'), 'publishedDate': volume_info.get(
                    'publishedDate'),
                    'pageCount': volume_info.get('pageCount'),
                    'rating': volume_info.get('averageRating'), 'annotation':
                        volume_info.get('description')
                    }
            all_books.append(data)
        return all_books
