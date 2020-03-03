from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
from core.models import VideoSubmission
from django.conf import settings
import pysrt


# from django.conf import settings
# import os

@shared_task
def process_video(video_id):
    folder_path = os.path.join(settings.MEDIA_ROOT, video_id)
    os.chdir(folder_path)
    subs = pysrt.open('subtitle.srt', encoding='iso-8859-1')
    chunk_directory = os.path.join(folder_path, 'chunks')
    os.mkdir(chunk_directory)
    os.system('ffmpeg -i video.mp4 -c copy -an nosound.mp4')
    os.system('ffmpeg -i video.mp4 -vn music.mp3')
    for i in range(len(subs)):
        start_time = str(subs[i].start).replace(',', '.')
        end_time = str(subs[i].end).replace(',', '.')
        video_file_name = chunk_directory + "/" + str(i) + '.mp4'
        audio_file_name = chunk_directory + "/" + str(i) + '.mp3'

        print(start_time)
        print(end_time)
        command = str("ffmpeg -i nosound.mp4 -ss " + start_time +
                      " -to " + end_time + " -async 1 " + video_file_name)
        os.system(command)
        command = str("ffmpeg -i music.mp3 -ss " + start_time +
                      " -to " + end_time + " -async 1 " + audio_file_name)
        print("-----------------------")

    print(len(subs))
    # ffmpeg - i
    # this.mp4 - c
    # copy - an
    # nosound.mp4
    VideoSubmission.objects.filter(pk=video_id).update(status='chunks')
