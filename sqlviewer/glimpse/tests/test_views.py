# Create your tests here.
import json
import os
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from sqlviewer.glimpse.models import Model, Version

from django.test import TestCase, Client
from sqlviewer.glimpse.services import save_imported_model
from django.conf import settings


class GlimpseViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='test', password='test')

        # Every test needs a client.
        self.client = Client()
        self.client.force_login(user)
        with open(os.path.join(os.path.dirname(__file__), 'resources/model.json')) as fin:
            data = json.load(fin)
        save_imported_model(data['model'])

    def test_search_view(self):
        version = Version.objects.first()
        url = reverse('version_search', args=(version.model.id, version.id))
        resp = self.client.post(url, data={'query': 'Product'})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, len(resp.context['results']))

    def test_search_view_uauthorized(self):
        version = Version.objects.first()
        url = reverse('version_search', args=(version.model.id, version.id))
        expected_redirect = "{0}?next={1}".format(settings.LOGIN_URL, url)
        resp = Client().post(url, data={'query': 'Product'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual(expected_redirect, resp.url)
