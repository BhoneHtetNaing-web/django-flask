from celery import Celery
from flask import send_email

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.timezone = "Asia/Yangon"

@celery.task
def send_email_task(to, subject, body):
    send_email(to, subject, body)

    send_email_task.delay("user@gmail.com", "Welcome to My World", "Hi")