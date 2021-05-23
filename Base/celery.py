import os
from celery import Celery
from collections import OrderedDict
from datetime import datetime, timedelta
import json
import environ

ENV = environ.Env()
environ.Env.read_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", ENV("DJANGO_SETTINGS_MODULE"))

app = Celery("Base")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        5.0,
        create_top_requests_per_day.s(),
    )


app.conf.timezone = 'UTC'


@app.task
def create_top_requests_per_day():
    from api.models import RequestModel
    COUNT_OF_TOP_REQUESTS_PER_DAY = 5
    LENGTH_TOP_REQUESTS_NUMBER_LIST = 8
    time_now = datetime.now()
    number_of_query_list, top_requests_texts = [], []
    time_threshold = time_now - timedelta(days=1)
    request_list = RequestModel.objects.filter(timestamp__gte=time_threshold)
    top_requests_texts = create_topics_list_by_time_interval(RequestModel, time_threshold)
    for text in top_requests_texts:
        number_of_query_list.append(create_topics_count_list_per_week(
            text=text, request_list=request_list, time_now=time_now))
    number_of_query_list = append_list_with_empty_lists(
        number_of_query_list, COUNT_OF_TOP_REQUESTS_PER_DAY, LENGTH_TOP_REQUESTS_NUMBER_LIST)
    top_requests_texts = append_list_with_empty_strings(top_requests_texts,
                                                        COUNT_OF_TOP_REQUESTS_PER_DAY)
    json_data = {"day": {"numberOfQuery": number_of_query_list,
                         "queryContent": top_requests_texts}}
    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


@app.task
def create_top_requests_per_week():
    from api.models import RequestModel
    COUNT_OF_TOP_REQUESTS_PER_WEEK = 5
    LENGTH_TOP_REQUESTS_NUMBER_LIST = 7
    time_now = datetime.now()
    number_of_query_list, top_requests_texts = [], []
    time_threshold = time_now - timedelta(days=7)
    request_list = RequestModel.objects.filter(timestamp__gte=time_threshold)
    top_requests_texts = create_topics_list_by_time_interval(RequestModel, time_threshold)
    for text in top_requests_texts:
        number_of_query_list.append(create_topics_count_list_per_week(
            text=text, request_list=request_list, time_now=time_now))
    number_of_query_list = append_list_with_empty_lists(
        number_of_query_list, COUNT_OF_TOP_REQUESTS_PER_WEEK, LENGTH_TOP_REQUESTS_NUMBER_LIST)
    top_requests_texts = append_list_with_empty_strings(top_requests_texts,
                                                        COUNT_OF_TOP_REQUESTS_PER_WEEK)
    json_data = {"week": {"numberOfQuery": number_of_query_list,
                         "queryContent": top_requests_texts}}
    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


@app.task
def create_top_requests_per_month():
    from api.models import RequestModel
    COUNT_OF_TOP_REQUESTS_PER_MONTH = 5
    LENGTH_TOP_REQUESTS_NUMBER_LIST = 4
    time_now = datetime.now()
    number_of_query_list, top_requests_texts = [], []
    time_threshold = time_now - timedelta(weeks=4)
    request_list = RequestModel.objects.filter(timestamp__gte=time_threshold)
    top_requests_texts = create_topics_list_by_time_interval(RequestModel, time_threshold)
    for text in top_requests_texts:
        number_of_query_list.append(create_topics_count_list_per_month(
            text=text, request_list=request_list, time_now=time_now))
    number_of_query_list = append_list_with_empty_lists(
        number_of_query_list, COUNT_OF_TOP_REQUESTS_PER_MONTH, LENGTH_TOP_REQUESTS_NUMBER_LIST)
    top_requests_texts = append_list_with_empty_strings(top_requests_texts,
                                                        COUNT_OF_TOP_REQUESTS_PER_MONTH)
    json_data = {"month": {"numberOfQuery": number_of_query_list,
                         "queryContent": top_requests_texts}}
    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def create_topics_count_list_per_day(text, request_list, time_now):
    THREE_HOURS_AGO_COEF = 1
    ONE_DAY_AGO_COEF = 9
    TIME_INTERVAL = 3
    number_list = []
    for time_coef in range(THREE_HOURS_AGO_COEF, ONE_DAY_AGO_COEF):
        time_left = time_now - timedelta(hours=TIME_INTERVAL * time_coef)
        time_right = time_now - timedelta(hours=TIME_INTERVAL * (time_coef - 1))
        request_list_per_current_interval = request_list.filter(
            text=text, timestamp__range=[time_left, time_right])
        number_list.append(request_list_per_current_interval.count())
    number_list.reverse()
    return number_list


def create_topics_count_list_per_week(text, request_list, time_now):
    number_list = []
    for day in range(1, 8):
        time_left = time_now - timedelta(days=day)
        time_right = time_now - timedelta(days=day - 1)
        request_list_per_current_interval = request_list.filter(
            text=text, timestamp__range=[time_left, time_right])
        number_list.append(request_list_per_current_interval.count())
    number_list.reverse()
    return number_list


def create_topics_count_list_per_month(text, request_list, time_now):
    number_list = []
    for week in range(1, 5):
        time_left = time_now - timedelta(weeks=week)
        time_right = time_now - timedelta(weeks=week - 1)
        request_list_per_current_interval = request_list.filter(
            text=text, timestamp__range=[time_left, time_right])
        number_list.append(request_list_per_current_interval.count())
    number_list.reverse()
    return number_list


def create_topics_list_by_time_interval(model, time_interval):
    top_requests = {}
    top_requests_texts = []
    for request in model.objects.filter(timestamp__gte=time_interval):
        top_requests[request.text] = top_requests.get(request.text, 0) + 1
    sorted_request_dict = (OrderedDict(sorted(top_requests.items(), key=lambda t: t[1])))
    for request in list(sorted_request_dict.items())[-5:]:
        top_requests_texts.append(request[0])
    return top_requests_texts


def append_list_with_empty_lists(request_number_list, list_length, empty_list_length):
    for _ in (range(list_length - len(request_number_list))):
        request_number_list.append([0 for i in range(empty_list_length)])
    return request_number_list


def append_list_with_empty_strings(query_content_list, list_length):
    for _ in (range(list_length - len(query_content_list))):
        query_content_list.append("")
    return query_content_list
