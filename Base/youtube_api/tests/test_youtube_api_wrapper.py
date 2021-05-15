from django.test import TestCase
from Base.youtube_api.youtube_api_wrapper import YoutubeApiWrapper


class YoutubeApiWrapperTestCase(TestCase):
    TEST_CHANNEL_TITLE = 'Tusur'

    def setUp(self):
        self.wrapper = YoutubeApiWrapper()

    def test_wrapper_get_response(self):
        self.wrapper.search_youtube_channels_by_keyword(self.TEST_CHANNEL_TITLE)
        self.assertTrue(self.wrapper.youtube_channel_list_data)

    def test_wrapper_correctly_parse_data(self):
        channel_keys_list = ["channel_url", "channel_title",
                             "channel_description", "channel_image",
                             "subscriber_count", "video_count:"]
        self.wrapper.search_youtube_channels_by_keyword(self.TEST_CHANNEL_TITLE)
        channel_data = self.wrapper.get_channels_data()["channel 0"]
        for key in channel_keys_list:
            if key not in channel_data.keys():
                self.assertTrue(False)
