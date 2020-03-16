from uuid import UUID

from core.models import VideoSubmission, VideoChunk
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status, exceptions
from rest_framework.response import Response

from .serializers import VideoSerializer, \
    VideoChunkSerializer, ChangeAudioSerializer
from .tasks import process_video, change_audio


# API Endpoints
class VideoList(mixins.ListModelMixin,
                generics.GenericAPIView):
    """Endpoint to accept video and subtitle uploads"""
    queryset = VideoSubmission.objects.all()
    serializer_class = VideoSerializer

    def get(self, request, *args, **kwargs):
        """All the Videos and subtitles uploaded will be listed"""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """creating a new project"""
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            process_video.delay(obj.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetVideoChunk(generics.ListAPIView):
    """Endpoint that will list all chunks info of a video"""
    serializer_class = VideoChunkSerializer

    def get_queryset(self):
        """query from chunks who project id is provided as arguments """
        pk = self.kwargs['pk']
        try:
            uuid_obj = UUID(pk, version=4)
            print(uuid_obj)
            try:
                chunk = VideoChunk.objects.filter(VideoSubmission=pk)
                return chunk
            except VideoChunk.DoesNotExist:
                raise exceptions.NotFound('Invalid Video ID')
        except ValueError:
            raise exceptions.NotFound('Invalid Video ID')

    def get(self, request, *args, **kwargs):
        """Return all chunks for particular video"""
        pk = self.kwargs['pk']
        try:
            video_obj = VideoSubmission.objects.get(pk=pk)
            chunk = VideoChunk.objects.filter(VideoSubmission=pk)
            context = {'request': request}

            ser_video = VideoSerializer(video_obj, context=context)
            ser_chunk = VideoChunkSerializer(chunk, many=True, context=context)

            return Response({
                'video_data': ser_video.data,
                'chunks': ser_chunk.data})
        except ValidationError:
            return Response(
                {"details": 'error'},
                status=status.HTTP_400_BAD_REQUEST)


class ChangeAudio(generics.RetrieveUpdateAPIView):
    """End point to change audio of a particular chunk"""
    serializer_class = ChangeAudioSerializer
    queryset = VideoChunk.objects.all()

    def get_object(self):
        """it will return chunk with provided arguments"""
        try:
            return VideoChunk.objects.get(VideoSubmission=self.kwargs['pk'],
                                          chunk_no=self.kwargs['chunk_no'])
        except VideoChunk.DoesNotExist:
            raise Http404

    def update(self, request, *args, **kwargs):
        """it will upload the new audio of specified chunk"""
        instance = self.get_object()
        instance.audio_chunk = request.data.get('audio_chunk')
        instance.save()
        serializer = ChangeAudioSerializer(instance)
        change_audio.delay(instance.VideoSubmission.id, instance.chunk_no)
        return Response(serializer.data)
