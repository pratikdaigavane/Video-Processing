from core.models import VideoSubmission
from .serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from .tasks import process_video


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
