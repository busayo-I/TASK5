from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient

class VideoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_video(self):
        # Provide the required fields in the request data
        data = {
            "title": "Test Video",
            "description": "Test Description",
            "Video_file": ''  # Use an empty string as a placeholder
        }
        response = self.client.post('/api/create_video/', data)
        print(response.status_code)
        print(response.content)
        print(response.headers)
        self.assertEqual(response.status_code, 201)
