# Create your tests here.
import json
import os
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from sqlviewer.viewer.services import save_imported_model


def import_model():
    with open(os.path.join(os.path.dirname(__file__), 'resources/model.json')) as fin:
        data = json.load(fin)
    save_imported_model(data['model'])


class RestAPITest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        import_model()

    def test_get_diagrams_ok(self):
        # Issue a GET request.
        model_id = "EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6"
        response = self.client.get('/api/v1/models/{0}/diagrams'.format(model_id))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_get_diagrams_not_exist(self):
        response = self.client.get('/api/v1/models/123B3E5E-7DC4-4BC9-9D35-C9A75372A123/diagrams')
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
        model_id = "23B3E5E-7DC4-4BC9-9D35-C9A75372A123"
        response = self.client.get(reverse('model_details', kwargs={"model_id": model_id}))
        self.assertEqual(response.status_code, 404)
