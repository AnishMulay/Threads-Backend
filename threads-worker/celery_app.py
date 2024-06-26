from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery = Celery(
    'threads-worker',
    broker=os.getenv('CELERY_BROKER_URL'),
)
celery.config_from_object('celeryconfig')

@celery.task
def process_item(item_id):
    print(f'Processing item with id {item_id}')

@celery.task
def example_task(x, y):
    return x + y
