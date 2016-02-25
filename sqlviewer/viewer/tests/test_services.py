from unittest import TestCase

from sqlviewer.viewer.services import get_diagram_details

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


class TestViewerServices(TestCase):
    def test_get_diagram_details(self):
        diagram = get_diagram_details("EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6",
                                      "E2711908-D8F4-4BF2-BE15-7FF62FAD5A5D")

        self.assertEqual("EER Diagram", diagram['name'])
        self.assertEqual(2, len(diagram['layers']))

        data = diagram['data']
        self.assertEqual("")
        pass
