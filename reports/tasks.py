from celery import shared_task
from .utils import generate_report_sync

@shared_task(bind=True)
def generate_report_from_submission(self, generated_report_id):
    """
    Celery task wrapper. Keeps the async path but delegates to the synchronous helper.
    """
    return generate_report_sync(generated_report_id)