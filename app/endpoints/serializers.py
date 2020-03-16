from core.models import VideoSubmission, VideoChunk
from rest_framework import serializers


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Single Video Submission"""

    class Meta:
        model = VideoSubmission
        fields = ['id', 'status', 'project_name',
                  'video', 'subtitle', 'total_chunks', 'processed_video']
        read_only_fields = ['id', 'status', 'total_chunks', 'processed_video']


class VideoChunkSerializer(serializers.ModelSerializer):
    """Serializer to list all chunks of a particular project"""

    class Meta:
        model = VideoChunk
        fields = [
            'chunk_no',
            'video_chunk',
            'audio_chunk',
            'start_time',
            'end_time',
            'subtitle'
        ]


class ChangeAudioSerializer(serializers.ModelSerializer):
    """Serializer to upload new audio for a particular chunk"""
    audio_chunk = serializers.SerializerMethodField('get_audio_chunk')

    def get_audio_chunk(self, obj):
        return obj.audio_chunk.url

    class Meta:
        model = VideoChunk
        fields = [
            'chunk_no',
            'video_chunk',
            'audio_chunk',
            'start_time',
            'end_time',
            'subtitle',
            'VideoSubmission'
        ]
        read_only_fields = [
            'chunk_no',
            'video_chunk',
            'start_time',
            'end_time',
            'subtitle',
            'VideoSubmission'
        ]
