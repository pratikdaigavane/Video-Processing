from django.db import models
import uuid
import os
from django.core.exceptions import ValidationError
from django.conf import settings

def get_video_chunk_path(instance, filename):
    if (not instance.project_id) and (not instance.chunk_no):
        raise ValidationError('Invalid Project ID')
    return os.path.join(instance.project_id + '/chunks/' + instance.chunk_no + '.mp4')


def get_audio_chunk_path(instance, filename):
    if (not instance.project_id) and (not instance.chunk_no):
        raise ValidationError('Invalid Project ID')
    return os.path.join(instance.project_id + '/chunks/' + instance.chunk_no + '.mp3')


def create_with_pk(self):
    instance = self.create()
    instance.save()
    return instance


def get_video_path(instance, filename):
    if not instance.pk:
        create_with_pk(instance)
    uid = str(instance.pk)
    ext = filename.split('.')[-1]
    return os.path.join(uid + '/video.' + ext)


def get_subtitle_path(instance, filename):
    if not instance.pk:
        create_with_pk(instance)
    uid = str(instance.pk)
    ext = filename.split('.')[-1]
    return os.path.join(uid + '/subtitle.' + ext)


def validate_video(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_subtitle(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.srt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def chunk_path():
    return os.path.join(settings.MEDIA_ROOT)


# Create your models here
class VideoSubmission(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    project_name = models.TextField(blank=False)
    status = models.CharField(default='in_queue', max_length=10)
    video = models.FileField(upload_to=get_video_path,
                             validators=[validate_video])
    subtitle = models.FileField(upload_to=get_subtitle_path,
                                validators=[validate_subtitle])

    def __str__(self):
        return str(self.pk)


class VideoChunk(models.Model):
    chunk_no = models.SmallIntegerField()
    VideoSubmission = models.ForeignKey(VideoSubmission, on_delete=models.CASCADE)
    video_chunk = models.FileField()
    audio_chunk = models.FileField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subtitle = models.TextField()
