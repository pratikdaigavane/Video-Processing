from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

LIST_URL = reverse('video-list')


class VideoChunkApiTests(TestCase):
    """Test for /video/projectId"""

    def setUp(self):
        self.client = APIClient()
        video = open('/app/endpoints/tests/jellies.mp4', 'rb')
        subtitle = open('/app/endpoints/tests/jellies.srt', 'rb')
        project_name = 'Test Project'
        payload = {
            'project_name': project_name,
            'video': video,
            'subtitle': subtitle
        }

        res = self.client.post(LIST_URL, payload)
        self.project_id = res.data['id']

    def test_get_chunk_list(self):
        """Test to get chunk list for particular video"""
        chunk_list_url = reverse('chunk-list', kwargs={'pk': self.project_id})
        res = self.client.get(chunk_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
