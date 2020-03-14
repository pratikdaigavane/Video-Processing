from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
from core.models import VideoSubmission, VideoChunk
from django.conf import settings
import pysrt
import pickle


@shared_task
def process_video(video_id):
    folder_path = os.path.join(settings.MEDIA_ROOT, video_id)
    os.chdir(folder_path)
    chunk_directory = os.path.join(folder_path, 'chunks')
    os.mkdir(chunk_directory)

    chunk_filename = []

    subs = pysrt.open('subtitle.srt', encoding='iso-8859-1')
    VideoSubmission.objects.filter(pk=video_id).update(total_chunks=len(subs))

    os.system('ffmpeg -i video.mp4 -c copy -an nosound.mp4')
    os.system('ffmpeg -i video.mp4 -vn music.mp3')
    for i in range(len(subs)):
        sub_text = str(subs[i].text)
        start_time = str(subs[i].start).replace(',', '.')
        end_time = str(subs[i].end).replace(',', '.')
        nos_video_file_name = chunk_directory + "/" + 'h_' + str(i) + '.mp4'
        nos_audio_file_name = chunk_directory + "/" + 'h_' + str(i) + '.mp3'
        # for the first video without subtitle
        if (i == 0) and (start_time != '00:00:00.000'):
            command = str(
                "ffmpeg  -i nosound.mp4 -ss 00:00:00.000 " +
                " -to " + start_time +
                " -async 1 " + nos_video_file_name)
            print(str(i) + " => " + command, flush=True)
            os.system(command)
            command = str(
                "ffmpeg  -i music.mp3 -ss 00:00:00.000 " +
                " -to " + start_time +
                " -c copy " + nos_audio_file_name)
            os.system(command)
            chunk_filename.append('h_' + str(i))

        # for the video with subtitle
        video_file_name = chunk_directory + "/" + str(i) + '.mp4'
        audio_file_name = chunk_directory + "/" + str(i) + '.mp3'
        command = str("ffmpeg -i nosound.mp4 -ss "
                      + start_time +
                      " -to " + end_time + " -async 1 " + video_file_name)
        print(str(i) + " => " + command, flush=True)

        os.system(command)
        command = str("ffmpeg -i music.mp3 -ss "
                      + start_time +
                      " -to " + end_time + " -c copy " + audio_file_name)
        os.system(command)
        chunk_filename.append(str(i))

        VideoChunk.objects.create(
            chunk_no=i,
            VideoSubmission=VideoSubmission.objects.get(id=video_id),
            video_chunk=os.path.join(video_id, 'chunks', str(i) + '.mp4'),
            audio_chunk=os.path.join(video_id, 'chunks', str(i) + '.mp3'),
            start_time=start_time,
            end_time=end_time,
            subtitle=sub_text
        )

        if (i != len(subs) - 1) and (i != 0):
            nos_start_time = str(subs[i].end).replace(',', '.')
            nos_end_time = str(subs[i + 1].start).replace(',', '.')
            if nos_start_time != nos_end_time:
                command = str("ffmpeg -i nosound.mp4 -ss "
                              + nos_start_time +
                              " -to " + nos_end_time +
                              " -async 1 " +
                              nos_video_file_name)
                print(str(i) + " => " + command, flush=True)

                os.system(command)
                command = str("ffmpeg -i music.mp3 -ss "
                              + nos_start_time +
                              " -to " + nos_end_time +
                              " -c copy " +
                              nos_audio_file_name)
                os.system(command)
                chunk_filename.append('h_' + str(i))
        if i == len(subs) - 1:
            command = str(
                "ffmpeg  -i nosound.mp4" +
                " -ss " + end_time +
                " -async 1 " + nos_video_file_name)
            print(str(i) + " => " + command, flush=True)
            os.system(command)
            command = str(
                "ffmpeg  -i music.mp3 -ss " + end_time +
                " -c copy " + nos_audio_file_name)
            os.system(command)
            chunk_filename.append('h_' + str(i))

        print("-----------------------")

    with open("chunks/filenames.txt", "wb") as fp:  # Pickling
        pickle.dump(chunk_filename, fp)

    change_all_audio(video_id)


@shared_task()
def change_all_audio(video_id):
    folder_path = os.path.join(settings.MEDIA_ROOT, video_id)
    chunk_directory = os.path.join(folder_path, 'chunks')
    os.chdir(chunk_directory)
    compile_video_list = open('compiled_video_list.txt', 'w+')

    with open("filenames.txt", "rb") as fp:  # Unpickling
        filenames = pickle.load(fp)
    print(filenames)
    for file in filenames:
        command = 'ffmpeg -y -i ' + \
                  file + '.mp4 -i ' + \
                  file + '.mp3 -c copy -shortest compiled_' + \
                  file + '.mp4'
        compile_video_list.write("file '" + 'compiled_' +
                                 file + '.mp4' + "'\n")

        os.system(command)
    compile_video_list.close()
    compile_all_chunks(video_id)


@shared_task()
def change_audio(video_id, chunk_no):
    VideoSubmission.objects.filter(pk=video_id).update(status='in_queue')
    chunk_no = str(chunk_no)
    folder_path = os.path.join(settings.MEDIA_ROOT, video_id)
    chunk_directory = os.path.join(folder_path, 'chunks')
    os.chdir(chunk_directory)
    command = 'ffmpeg -y -i ' + chunk_no + \
              '.mp4 -i ' + chunk_no + \
              '.mp3 -c copy -shortest compiled_' + \
              chunk_no + '.mp4 '
    os.system(command)
    compile_all_chunks(video_id)


@shared_task()
def compile_all_chunks(video_id):
    folder_path = os.path.join(settings.MEDIA_ROOT, video_id)
    chunk_directory = os.path.join(folder_path, 'chunks')
    os.chdir(chunk_directory)
    command = 'ffmpeg -y -f concat -safe 0 -i ' \
              'compiled_video_list.txt -c copy fully_final.mp4'
    os.system(command)
    VideoSubmission.objects.filter(pk=video_id).update(status='done')
