from celery import shared_task
from .play.testing import mainLoop


@shared_task
def play_task(username):
    mainLoop(username)
    return None
