from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

LIST_URL = reverse('video-list')


class VideoListApiTests(TestCase):
    """Test the /video api"""

    def setUP(self):
        self.client = APIClient()

    def test_list_all_video(self):
        """test retrieving all videos"""
        res = self.client.get(LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_upload_new_video(self):
    #     """test which uploads new file"""
    #     video = open('/app/endpoints/tests/jellies.mp4', 'rb')
    #     subtitle = open('/app/endpoints/tests/jellies.srt', 'rb')
    #     project_name = 'Test Project'
    #     payload = {
    #         'project_name': project_name,
    #         'video': video,
    #         'subtitle': subtitle
    #     }
    #     res = self.client.post(LIST_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
