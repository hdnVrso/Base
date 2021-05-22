import os
from celery import Celery
from collections import OrderedDict
from datetime import datetime, timedelta
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Base.settings")

app = Celery("Base")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        5.0,
        get_top.s(),
    )


app.conf.timezone = 'UTC'


@app.task
def get_top():
    from authentication.models import RequestModel
    COUNT_OF_TOP_REQUESTS_PER_DAY = 5
    time_now = datetime.now()
    number_of_query_list, query_content_list, top_requests_texts = [], [], []
    time_threshold = time_now - timedelta(days=1)
    request_list = RequestModel.objects.filter(timestamp__gte=time_threshold)
    top_requests_texts = create_topics_list_by_time_interval(RequestModel, time_threshold)
    for text in top_requests_texts:
        number_of_query_list.append(create_time_interval_list_of_counts_for_request(
            text=text, request_list=request_list, time_now=time_now))
    json_data = {"day": {"numberOfQuery": number_of_query_list,
                         "queryContent": top_requests_texts}}
    input_empty_lists_to_request_number_list(number_of_query_list, 5, 8)
    input_empty_strings_to_query_content_list(top_requests_texts, 5)
    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def create_time_interval_list_of_counts_for_request(text, request_list, time_now):
    from authentication.models import RequestModel
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


def create_topics_list_by_time_interval(model, time_interval):
    top_requests = {}
    top_requests_texts = []
    for request in model.objects.filter(timestamp__gte=time_interval):
        top_requests[request.text] = top_requests.get(request.text, 0) + 1
    sorted_request_dict = (OrderedDict(sorted(top_requests.items(), key=lambda t: t[1])))
    for request in list(sorted_request_dict.items())[-5:]:
        top_requests_texts.append(request[0])
    return top_requests_texts


def input_empty_lists_to_request_number_list(request_number_list, list_length, empty_list_length):
    for _ in (range(list_length - len(request_number_list))):
        request_number_list.append([0 for i in range(empty_list_length)])


def input_empty_strings_to_query_content_list(query_content_list, list_length):
    for _ in (range(list_length - len(query_content_list))):
        query_content_list.append("")
