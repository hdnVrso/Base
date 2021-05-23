from django.test import TestCase
from Base.celery import append_list_with_empty_lists, append_list_with_empty_strings, \
    create_topics_list_by_time_interval
from datetime import datetime, timedelta
from api.models import RequestModel
from authentication.models import User


class CeleryTestCase(TestCase):
    TEST_LIST_LENGTH = 3
    TEST_EMPTY_LIST_LENGTH = 3

    def test_append_list_with_empty_lists(self):
        TEST_RESULT = [[0 for _ in range(self.TEST_EMPTY_LIST_LENGTH)]
                       for _ in range(self.TEST_LIST_LENGTH)]
        TEST_LIST = []
        self.assertEquals(TEST_RESULT, append_list_with_empty_lists(
            TEST_LIST, self.TEST_LIST_LENGTH, self.TEST_EMPTY_LIST_LENGTH))

    def test_append_list_with_empty_strings(self):
        TEST_RESULT = ["" for _ in range(self.TEST_LIST_LENGTH)]
        TEST_LIST = []
        self.assertEquals(TEST_RESULT, append_list_with_empty_strings(
            TEST_LIST, self.TEST_LIST_LENGTH))

    def test_create_topics_list_by_time_interval_day(self):
        TIME_INTERVAL_ONE_DAY = datetime.now() - timedelta(days=1)
        TEST_LENGTH = 10
        TEST_CREDENTIALS = ('testusername', 'testemail@test.com', 'TestPass1234')
        TEST_USER = User.objects.create_user(TEST_CREDENTIALS[0], TEST_CREDENTIALS[1],
                                             TEST_CREDENTIALS[2])
        TEST_RESULT = [f'test_request_{i}' for i in range(1, 5)]
        for i in range(TEST_LENGTH):
            for _ in range(i):
                new_model = RequestModel(user=TEST_USER, text=f'test_request_{i}')
                new_model.timestamp = new_model.timestamp - timedelta(hours=i * 5)
                new_model.save()
        self.assertEquals(TEST_RESULT, create_topics_list_by_time_interval(
            RequestModel, TIME_INTERVAL_ONE_DAY))

    def test_create_topics_list_by_time_interval_week(self):
        TIME_INTERVAL_ONE_WEEK = datetime.now() - timedelta(weeks=1)
        TEST_LENGTH = 10
        TEST_CREDENTIALS = ('testusername', 'testemail@test.com', 'TestPass1234')
        TEST_USER = User.objects.create_user(TEST_CREDENTIALS[0], TEST_CREDENTIALS[1],
                                             TEST_CREDENTIALS[2])
        TEST_RESULT = [f'test_request_{i}' for i in range(1, 4)]
        for i in range(TEST_LENGTH):
            for _ in range(i):
                new_model = RequestModel(user=TEST_USER, text=f'test_request_{i}')
                new_model.timestamp = new_model.timestamp - timedelta(days=i * 2)
                new_model.save()
        self.assertEquals(TEST_RESULT, create_topics_list_by_time_interval(
            RequestModel, TIME_INTERVAL_ONE_WEEK))

    def test_create_topics_list_by_time_interval_month(self):
        TIME_INTERVAL_ONE_MONTH = datetime.now() - timedelta(weeks=4)
        TEST_LENGTH = 10
        TEST_CREDENTIALS = ('testusername', 'testemail@test.com', 'TestPass1234')
        TEST_USER = User.objects.create_user(TEST_CREDENTIALS[0], TEST_CREDENTIALS[1],
                                             TEST_CREDENTIALS[2])
        TEST_RESULT = [f'test_request_{i}' for i in range(1, 5)]
        for i in range(TEST_LENGTH):
            for _ in range(i):
                new_model = RequestModel(user=TEST_USER, text=f'test_request_{i}')
                new_model.timestamp = new_model.timestamp - timedelta(weeks=i)
                new_model.save()
        self.assertEquals(TEST_RESULT, create_topics_list_by_time_interval(
            RequestModel, TIME_INTERVAL_ONE_MONTH))
