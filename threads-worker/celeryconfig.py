import os

broker_url = os.getenv('CELERY_BROKER_URL')
result_backend = None

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

worker_prefetch_multiplier = 1
task_acks_late = True