import json
from unittest import TestCase
from sqlviewer.integration import mysqlwb
from sqlviewer.integration.mysqlwb import convert_workbench_size
from tests.util import get_resource_path

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
