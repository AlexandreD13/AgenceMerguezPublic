import os

from celery import Celery
from django.apps import apps

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agence.settings')

app = Celery(
    'agence',
    # Nb of workers
    worker_concurrency=1,
    worker_max_tasks_per_child=1,
    # Max memory per worker (4mb)
    worker_max_memory_per_child=4000,
    worker_prefetch_multiplier=1
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
