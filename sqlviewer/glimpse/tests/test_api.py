import json
import os
from django.contrib.auth.models import User
from django.test import Client
from django.test.testcases import TestCase
from sqlviewer.glimpse.services import save_imported_model

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


class GlimpseApiViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='test', password='test')

        # Every test needs a client.
        self.client = Client()
        self.client.force_login(user)
        with open(os.path.join(os.path.dirname(__file__), 'resources/model.json')) as fin:
            data = json.load(fin)
        save_imported_model(data['model'])

    def test_api_get_model_list(self):
        response = self.client.get('/api/v1/models/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual("EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6".lower(), data[0]['id'])
        self.assertEqual("name", data[0]['name'])

    def test_api_get_model(self):
        response = self.client.get('/api/v1/models/1')
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual("EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6".lower(), data['id'])
        self.assertEqual("name", data['name'])
        self.assertEqual(1, len(data['versions']))
        self.assertEqual(0, data['versions'][0]['number'])
        self.assertEqual('version', data['versions'][0]['label'])

    def test_api_get_version_list(self):
        response = self.client.get('/api/v1/models/1/versions/')
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(1, len(data))
        self.assertEqual(0, data[0]['number'])
        self.assertEqual('version', data[0]['label'])

    def test_api_get_version(self):
        response = self.client.get('/api/v1/models/1/versions/1')
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(0, data['number'])
        self.assertEqual('version', data['label'])
        self.assertEqual(2, len(data['diagrams']))
        diagram = data['diagrams'][0]
        self.assertEqual('1ABE0B5E-152C-48A0-AF62-B865324F28FC'.lower(), diagram['id'])
        self.assertEqual('Core', diagram['name'])
        diagram = data['diagrams'][1]
        self.assertEqual('E2711908-D8F4-4BF2-BE15-7FF62FAD5A5D'.lower(), diagram['id'])
        self.assertEqual('EER Diagram', diagram['name'])

    def test_api_get_diagram_list(self):
        response = self.client.get('/api/v1/models/1/versions/1/diagrams/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(2, len(data))
        diagram = data[0]
        self.assertEqual('1ABE0B5E-152C-48A0-AF62-B865324F28FC'.lower(), diagram['id'])
        self.assertEqual('Core', diagram['name'])
        diagram = data[1]
        self.assertEqual('E2711908-D8F4-4BF2-BE15-7FF62FAD5A5D'.lower(), diagram['id'])
        self.assertEqual('EER Diagram', diagram['name'])

    def test_api_get_diagram(self):
        response = self.client.get('/api/v1/models/1/versions/1/diagrams/1')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual('1ABE0B5E-152C-48A0-AF62-B865324F28FC'.lower(), data['id'])
        self.assertEqual('Core', data['name'])

        response = self.client.get('/api/v1/models/1/versions/1/diagrams/2')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual('E2711908-D8F4-4BF2-BE15-7FF62FAD5A5D'.lower(), data['id'])
        self.assertEqual('EER Diagram', data['name'])

        response = self.client.get('/api/v1/models/1/versions/1/diagrams/3')
        self.assertEqual(response.status_code, 404)
