from django.test import TestCase
from Base.youtube_api.youtube_api_wrapper import YoutubeApiWrapper


class YoutubeApiWrapperTestCase(TestCase):
    TEST_CHANNEL_TITLE = 'Tusur'

    def setUp(self):
        self.wrapper = YoutubeApiWrapper()

    def test_wrapper_get_response(self):
        self.wrapper.search_youtube_channels_by_keyword(self.TEST_CHANNEL_TITLE)
        self.assertTrue(self.wrapper.youtube_channel_list_data)
