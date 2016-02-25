# Create your tests here.
import unittest
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class RestAPITest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_get_diagrams_ok(self):
        # Issue a GET request.
        model_id = "EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6"
        response = self.client.get('/api/v1/models/{0}/diagrams'.format(model_id))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_get_diagrams_not_exist(self):
        response = self.client.get('/api/v1/models/fake-id/diagrams')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 404)


class ViewerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_model_details_page_ok(self):
        model_id = "EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6"
        response = self.client.get(reverse('model_details', kwargs={"model_id": model_id}))
        context = response.context

        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(context['diagrams']))
        self.assertEqual(model_id, context['model_id'])

    def test_model_details_page_model_not_found(self):
        model_id = "fake-model-id"
        response = self.client.get(reverse('model_details', kwargs={"model_id": model_id}))
        self.assertEqual(response.status_code, 404)
