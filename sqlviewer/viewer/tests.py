# Create your tests here.
import unittest
from django.test import TestCase, Client


class RestAPITest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/api/v1/models/1/diagrams')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
