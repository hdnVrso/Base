import os
from celery import Celery

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
    from collections import OrderedDict
    from datetime import datetime, timedelta
    import json
    COUNT_OF_TOP_REQUESTS_PER_DAY = 5
    time_now = datetime.now()
    top_requests = {}
    number_of_query_list, query_content_list, top_requests_texts = [], [], []
    time_threshold = time_now - timedelta(days=1)
    request_list = RequestModel.objects.filter(timestamp__gte=time_threshold)
    for request in request_list:
        top_requests[request.text] = top_requests.get(request.text, 0) + 1
    sorted_request_dict = (OrderedDict(sorted(top_requests.items(), key=lambda t: t[1])))
    print(sorted_request_dict)
    for request in list(sorted_request_dict.items())[-5:]:
        top_requests_texts.append(request[0])
    for text in top_requests_texts:
        number_of_query_list.append(create_time_interval_list_of_counts_for_request(
            text=text, request_list=request_list, time_now=time_now))
    for _ in (range(COUNT_OF_TOP_REQUESTS_PER_DAY - len(number_of_query_list))):
        number_of_query_list.append([0, 0, 0, 0, 0, 0, 0, 0])
    json_data = {"day": {"numberOfQuery": number_of_query_list,
                             "queryContent": top_requests_texts}}
    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def create_time_interval_list_of_counts_for_request(text, request_list, time_now):
    from authentication.models import RequestModel
    from collections import OrderedDict
    from datetime import datetime, timedelta
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
