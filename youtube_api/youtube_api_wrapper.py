from googleapiclient.discovery import build
import environ


class YoutubeApiWrapper:
    YOUTUBE_URL_PATTERN = 'https://www.youtube.com/channel/'

    def __init__(self):
        ENV = environ.Env()
        environ.Env.read_env()
        self.youtube_api_key = ENV('GOOGLE_API_KEY')
        self.youtube_channel_list_data = {}
        self.youtube_object = build('youtube', 'v3',
                                    developerKey=self.youtube_api_key)

    def search_youtube_channels_by_keyword(self, keyword, maxChannelCount=10):
        request = self.youtube_object.search().list(part="snippet",
                                                    q=keyword, type='channel',
                                                    maxResults=maxChannelCount)
        self.youtube_channel_list_data = request.execute()

    def get_detail_channel_info_by_channel_id(self, channel_id):
        return self.youtube_object.channels().list(part='snippet, statistics',
                                                   id=channel_id).execute()

    def get_channels_data(self):
        youtube_data = {}
        number = 0
        for channel in self.youtube_channel_list_data['items']:
            detail_channel_info = self.get_detail_channel_info_by_channel_id(
                channel['id']['channelId'])
            if not detail_channel_info['items'][0]['statistics']['hiddenSubscriberCount']:
                channel_data = {
                    'channel_url': YoutubeApiWrapper.YOUTUBE_URL_PATTERN
                    + channel['id']['channelId'],
                    'channel_title': channel['snippet']['title'],
                    'channel_description': channel['snippet']['description'],
                    'channel_image': channel['snippet']['thumbnails']
                    ['high']['url'],
                    'subscriber_count': detail_channel_info['items'][0]
                    ['statistics']['subscriberCount'],
                    'video_count:': detail_channel_info['items'][0]
                    ['statistics']['videoCount']}
                youtube_data.setdefault('channel {number}'.format(
                    number=number), channel_data)
                number += 1
        return youtube_data
