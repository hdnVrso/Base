from django.test import TestCase
from Base.celery import append_list_with_empty_lists, append_list_with_empty_strings


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


