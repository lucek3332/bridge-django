from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_task(subject, msg, sender, to):
    send_mail(subject, msg, sender, to)
    return None
