from celery import shared_task
from .play.client import mainLoop


@shared_task
def play_task(username):
    mainLoop(username)
    return None
