from rest_framework import serializers
from core.models import VideoSubmission


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSubmission
        fields = ['id', 'status', 'video', 'subtitle']
        read_only = ['id', 'status']
