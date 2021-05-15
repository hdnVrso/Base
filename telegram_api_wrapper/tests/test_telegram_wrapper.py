from django.test import TestCase
from telegram_api_wrapper.telegram_api_wrapper import TelegramApiWrapper


class Channel():
    def __init__(self):
        self.title = "title"
        self.participants_count = "90000"
        self.username = "username"
        self.channel_info = "about"


class WrapperTestCase(TestCase):
    def setUp(self):
        self.telegram = TelegramApiWrapper()

    def test_search_channels(self):
        query = "Python"
        result = self.telegram.search_channels(query)
        result_b = False
        if result[0]['title'].find(query) != -1:
            result_b = True
        self.assertTrue(result_b)

    def test_can_call_method_create_dict(self):
        try:
            channel = Channel()
            self.telegram.create_dict(channel, channel.channel_info)
        except BaseException:
            self.fail("create_dict raised ThatException")

    def test_can_create_dict(self):
        correct_dict = {'title': "title",
                        'members': "90000",
                        'link': "t.me/username",
                        'channel_info': "about"
                        }
        channel = Channel()
        result_dict = self.telegram.create_dict(channel, channel.channel_info)
        self.assertEqual(result_dict, correct_dict)
