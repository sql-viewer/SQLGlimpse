import json
from django.test import TestCase


# Create your tests here.
from os.path import join, dirname
from sqlviewer.connect.services import breadth_first_search, build_search_graph
from sqlviewer.glimpse.models import Version
from sqlviewer.glimpse.services import save_imported_model


class ConnectServiceTests(TestCase):
    def setUp(self):
        with open(join(dirname(dirname(dirname(__file__))), 'glimpse/tests/resources/model.json')) as fin:
            self.data = json.load(fin)['model']
        save_imported_model(self.data)

    def test_build_search_map(self):
        version = Version.objects.get(pk=1)
        map = build_search_graph(version)

    def test_connect_search(self):
        data = self.data
        graph = {'A': ['B', 'C'],
                 'B': ['C', 'D'],
                 'C': ['D'],
                 'D': ['C'],
                 'E': ['F'],
                 'F': ['C']}

        results = breadth_first_search(graph, 'A', 'D')
