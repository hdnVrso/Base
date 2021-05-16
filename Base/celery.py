import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Base.settings")


app = Celery("Base")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        3.0,
        sample_task.s(),
    )


app.conf.timezone = 'UTC'


@app.task
def sample_task():
    from authentication.models import RequestModel
    print(RequestModel.objects.all())