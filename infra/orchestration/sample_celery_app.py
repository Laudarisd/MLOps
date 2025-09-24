# sample_celery_app.py
"""
Sample Celery app for distributed task orchestration.
"""
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y

if __name__ == "__main__":
    result = add.delay(2, 3)
    print('Task result:', result.get())
