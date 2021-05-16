import os
from celery import Celery
from celery.schedules import crontab
from api.models.request_model import RequestModel

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Base.settings")

app = Celery("Base")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(),
        sample_task.s(),
    )


app.conf.timezone = 'UTC'

@app.task
def sample_task():
    pass
