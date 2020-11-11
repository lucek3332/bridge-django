from celery import shared_task
from game.client import mainLoop


@shared_task
def play_task(username):
    mainLoop(username)
    return None
