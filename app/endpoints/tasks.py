from __future__ import absolute_import, unicode_literals
from celery import shared_task
from time import sleep
from core.models import VideoSubmission


# from django.conf import settings
# import os

@shared_task
def process_video(video_id):
    sleep(5)
    print(video_id)
    VideoSubmission.objects.filter(pk=video_id).update(status='chunks')
