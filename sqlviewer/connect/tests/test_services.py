import json
from django.test import TestCase


# Create your tests here.
from os.path import join, dirname
from sqlviewer.connect.services import breadth_first_search


class ConnectServiceTests(TestCase):
    def setUp(self):
        with open(join(dirname(dirname(dirname(__file__))), 'glimpse/tests/resources/model-small.json')) as fin:
            self.data = json.load(fin)



    def test_connect_search(self):
        data = self.data
        graph = {'A': ['B', 'C'],
                 'B': ['C', 'D'],
                 'C': ['D'],
                 'D': ['C'],
                 'E': ['F'],
                 'F': ['C']}


        results = breadth_first_search(graph, 'A', 'D')
