import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models

from .storage import OverwriteStorage


def get_video_path(instance, filename):
    """
    Get path of uploaded video file
    the video file will be stored in "project_id/video.mp4" in media directory
    """
    if not instance.pk:
        create_with_pk(instance)
    uid = str(instance.pk)
    ext = filename.split('.')[-1]
    return os.path.join(uid + '/video.' + ext)


def get_subtitle_path(instance, filename):
    """
    Get path of uploaded video file
    the video file will be stored in "project_id/subtitle.mp4"
    in media directory
    """
    if not instance.pk:
        create_with_pk(instance)
    uid = str(instance.pk)
    ext = filename.split('.')[-1]
    return os.path.join(uid + '/subtitle.' + ext)


def create_with_pk(self):
    """create the Video Submission Object if not created initially"""
    instance = self.create()
    instance.save()
    return instance


def validate_video(value):
    """Checking if the uploaded video has .mp4 extension"""
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_subtitle(value):
    """Checking if the uploaded subtitle has .srt extension"""
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.srt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_audio(value):
    """Checking if the uploaded audio has .mp3 extension"""
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def get_video_chunk_path(instance, filename):
    """
    Get path to store video chunk
    the path will be of format : project_id/chunks/chunk_no.mp3
    """

    if (not instance.project_id) and (not instance.chunk_no):
        raise ValidationError('Invalid Project ID')
    return os.path.join(instance.project_id +
                        '/chunks/' +
                        instance.chunk_no +
                        '.mp4')


def get_audio_chunk_path(instance, filename):
    """
    Get path to store audio chunk
    the path will be of format : project_id/chunks/chunk_no.mp3
    """
    if (not instance.VideoSubmission.id) and (not instance.chunk_no):
        raise ValidationError('Invalid Project ID')
    return os.path.join(str(instance.VideoSubmission.id) +
                        '/chunks/' +
                        str(instance.chunk_no) +
                        '.mp3')


# Models
class VideoSubmission(models.Model):
    """
    This model holds video and subtitle uploaded by user
    after uploading, a project id will be allocate.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    project_name = models.TextField(blank=False)
    status = models.CharField(default='in_queue', max_length=10)
    video = models.FileField(upload_to=get_video_path,
                             validators=[validate_video])
    subtitle = models.FileField(upload_to=get_subtitle_path,
                                validators=[validate_subtitle])
    total_chunks = models.SmallIntegerField(default=0)
    processed_video = models.FileField()

    def __str__(self):
        return str(self.project_name)


class VideoChunk(models.Model):
    """
    This model hold processed video chunk
    It has many-to-one relationship with VideoSubmission Object
    """
    chunk_no = models.SmallIntegerField()
    VideoSubmission = models.ForeignKey(VideoSubmission,
                                        on_delete=models.CASCADE)
    video_chunk = models.FileField()
    audio_chunk = models.FileField(upload_to=get_audio_chunk_path,
                                   validators=[validate_audio],
                                   storage=OverwriteStorage())
    start_time = models.TimeField()
    end_time = models.TimeField()
    subtitle = models.TextField()
