import json
from unittest import TestCase
from sqlviewer.integration import mysqlwb
from tests.util import get_resource_path

__author__ = 'stefa'


class TestMySQLWbImport(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_import_model(self):
        model_path = get_resource_path('model/mysqlwb.mwb')
        data = mysqlwb.import_model(model_path, 'name', 'version')
        with open(get_resource_path('model/mysqlwb.json')) as fin:
            expected_data = json.load(fin)

        self.assertDictEqual(expected_data, data)
