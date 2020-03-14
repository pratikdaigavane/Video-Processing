from core.models import VideoSubmission, VideoChunk
from .serializers import VideoSerializer, \
    VideoChunkSerializer, ChangeAudioSerializer
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework import generics
from rest_framework import mixins
from .tasks import process_video, change_audio
from django.http import Http404

from uuid import UUID


# Create your views here.
class VideoList(mixins.ListModelMixin,
                generics.GenericAPIView):
    queryset = VideoSubmission.objects.all()
    serializer_class = VideoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            process_video.delay(obj.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetVideoChunk(generics.ListAPIView):
    serializer_class = VideoChunkSerializer

    def get_queryset(self):
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


class ChangeAudio(generics.RetrieveUpdateAPIView):
    serializer_class = ChangeAudioSerializer
    queryset = VideoChunk.objects.all()

    def get_object(self):
        try:
            return VideoChunk.objects.get(VideoSubmission=self.kwargs['pk'],
                                          chunk_no=self.kwargs['chunk_no'])
        except VideoChunk.DoesNotExist:
            raise Http404

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.audio_chunk = request.data.get('audio_chunk')
        instance.save()
        serializer = ChangeAudioSerializer(instance)
        print(instance.id)
        change_audio.delay(instance.VideoSubmission.id, instance.chunk_no)
        return Response(serializer.data)
