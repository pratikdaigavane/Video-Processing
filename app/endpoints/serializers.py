from rest_framework import serializers
from core.models import VideoSubmission, VideoChunk


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSubmission
        fields = ['id', 'status', 'project_name', 'video', 'subtitle']
        read_only_fields = ['id', 'status']


class VideoChunkSerializer(serializers.ModelSerializer):
    # video_chunk = serializers.SerializerMethodField('get_video_chunk_url')
    # audio_chunk = serializers.SerializerMethodField('get_audio_chunk_url')

    # def get_video_chunk_url(self, obj):
    #     print(obj.video_chunk)
    #     return obj.video_chunk
    #
    # def get_audio_chunk_url(self, obj):
    #     print(obj.video_chunk)
    #     return obj.audio_chunk

    class Meta:
        model = VideoChunk
        fields = ['chunk_no',
                  'video_chunk',
                  'audio_chunk',
                  'start_time',
                  'end_time',
                  'subtitle',
                  'VideoSubmission']
