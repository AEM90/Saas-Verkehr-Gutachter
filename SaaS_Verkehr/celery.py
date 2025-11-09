import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SaaS_Verkehr.settings")

app = Celery("SaaS_Verkehr")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()