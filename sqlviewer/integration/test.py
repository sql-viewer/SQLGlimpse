import json
from django.test import TestCase
from sqlviewer.integration import mysqlwb
from sqlviewer.integration.mysqlwb import convert_workbench_size, parse_column_information
from sqlviewer.integration.tests.util import get_resource_path, get_resource_content

from xml.etree import ElementTree as ET

__author__ = 'stefa'


class TestMySQLWbImport(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_import_model(self):
        model_path = get_resource_path('model/mysqlwb-small.mwb')
        data = mysqlwb.import_model(model_path, 'name', 'version')
        with open(get_resource_path('model/mysqlwb-small.json')) as fin:
            expected_data = json.load(fin)

        self.assertDictEqual(expected_data, data)

    def test_convert_size(self):
        self.assertEqual(330, convert_workbench_size("3.3e+002"))
        self.assertEqual(0, convert_workbench_size("0.e+002"))
        self.assertEqual(6902, convert_workbench_size("6.9020000000000009e+003"))

    def test_parse_column_information(self):
        column_element = ET.fromstring(get_resource_content('model/elements/column.xml'))
        col = parse_column_information(column_element, 'table', 0)

        self.assertEqual("70A39AC0-1194-4831-94B2-B663A2118C42", col['id'])
        self.assertEqual("CMN_PRO_ProductID", col['name'])
        self.assertEqual("table", col['tableId'])
        self.assertEqual("Special Comment", col['comment'])

        self.assertEqual(False, col['flags']['nullable'])
        self.assertEqual(False, col['flags']['hidden'])
        self.assertEqual(True, col['flags']['key'])
        self.assertEqual(False, col['flags']['autoIncrement'])
        self.assertEqual(False, col['flags']['reference'])
