from rest_framework import serializers
from core.models import VideoSubmission, VideoChunk


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSubmission
        fields = ['id', 'status', 'project_name', 'video', 'subtitle', 'total_chunks']
        read_only_fields = ['id', 'status', 'total_chunks']


class VideoChunkSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField('get_project_name')

    # audio_chunk = serializers.SerializerMethodField('get_audio_chunk_url')

    def get_project_name(self, obj):
        print(obj.VideoSubmission.project_name)
        return obj.VideoSubmission.project_name

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
                  'project_name',
                  'VideoSubmission']


class ChangeAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoChunk
        fields = ['chunk_no',
                  'video_chunk',
                  'audio_chunk',
                  'start_time',
                  'end_time',
                  'subtitle',
                  'VideoSubmission']
        read_only_fields = ['chunk_no',
                            'video_chunk',
                            'start_time',
                            'end_time',
                            'subtitle',
                            'VideoSubmission']
