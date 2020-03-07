from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
from core.models import VideoSubmission, VideoChunk
from django.conf import settings
import pysrt


@shared_task
def process_video(video_id):
    folder_path = os.path.join(settings.MEDIA_ROOT, video_id)
    os.chdir(folder_path)
    subs = pysrt.open('subtitle.srt', encoding='iso-8859-1')
    chunk_directory = os.path.join(folder_path, 'chunks')
    os.mkdir(chunk_directory)
    os.system('ffmpeg -i video.mp4 -c copy -an nosound.mp4')
    os.system('ffmpeg -i video.mp4 -vn music.mp3')
    os.system('touch meta_data.json')
    meta_file = []
    for i in range(len(subs)):
        sub_text = str(subs[i].text)
        start_time = str(subs[i].start).replace(',', '.')
        end_time = str(subs[i].end).replace(',', '.')
        video_file_name = chunk_directory + "/" + str(i) + '.mp4'
        audio_file_name = chunk_directory + "/" + str(i) + '.mp3'
        command = str("ffmpeg -i nosound.mp4 -ss " + start_time +
                      " -to " + end_time + " -async 1 " + video_file_name)
        os.system(command)
        command = str("ffmpeg -i music.mp3 -ss " + start_time +
                      " -to " + end_time + " -c copy " + audio_file_name)
        os.system(command)

        VideoChunk.objects.create(
            chunk_no=i,
            VideoSubmission=VideoSubmission.objects.get(id=video_id),
            video_chunk=os.path.join(video_id, 'chunks', str(i) + '.mp4'),
            audio_chunk=os.path.join(video_id, 'chunks', str(i) + '.mp3'),
            start_time=start_time,
            end_time=end_time,
            subtitle=sub_text
        )
        print("-----------------------")
    VideoSubmission.objects.filter(pk=video_id).update(status='done')
