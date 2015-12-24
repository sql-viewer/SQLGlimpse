import json
from django.test import TestCase
from sqlviewer.integration import mysqlwb
from sqlviewer.integration.mysqlwb import convert_workbench_size, parse_column_information, parse_layer_information, \
    parse_table_figure_information, parse_table_information, parse_diagram_information, parse_model_information
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
        element = ET.fromstring(get_resource_content('model/elements/column.xml'))
        col = parse_column_information(element, 'table', 0)

        self.assertEqual("70A39AC0-1194-4831-94B2-B663A2118C42", col['id'])
        self.assertEqual("CMN_PRO_ProductID", col['name'])
        self.assertEqual("table", col['tableId'])
        self.assertEqual("Special Comment", col['comment'])

        self.assertEqual(False, col['flags']['nullable'])
        self.assertEqual(False, col['flags']['hidden'])
        self.assertEqual(True, col['flags']['key'])
        self.assertEqual(False, col['flags']['autoIncrement'])
        self.assertEqual(False, col['flags']['reference'])

    def test_parse_layer_information(self):
        element = ET.fromstring(get_resource_content('model/elements/layer.xml'))
        layer = parse_layer_information(element)

        self.assertEqual("58A8526D-4C44-4896-A18E-EDBFFC7E7E4A", layer['id'])
        self.assertEqual([], layer['tables'])
        self.assertEqual("LayerName", layer['name'])
        self.assertEqual("LayerDescription", layer['description'])

        self.assertEqual(641, layer["element"]["x"])
        self.assertEqual(943, layer["element"]["y"])
        self.assertEqual(512, layer["element"]["width"])
        self.assertEqual(300, layer["element"]["height"])
        self.assertEqual("#F0F1FE", layer["element"]["color"])

    def test_parse_table_figure_information(self):
        element = ET.fromstring(get_resource_content('model/elements/table-figure.xml'))
        table = parse_table_figure_information(element)
        self.assertEqual("CA8DEB78-99DD-4EB3-9F40-DDE75431D7BB", table['id'])
        self.assertEqual("3709F0EB-A274-4A70-8119-7A3D198CC00D", table['tableId'])

        self.assertEqual(87, table["element"]["x"])
        self.assertEqual(37, table["element"]["y"])
        self.assertEqual(330, table["element"]["width"])
        self.assertEqual(190, table["element"]["height"])
        self.assertEqual(False, table["element"]["collapsed"])
        self.assertEqual("#98BFDA", table["element"]["color"])

    def test_parse_table_information(self):
        element = ET.fromstring(get_resource_content('model/elements/table.xml'))
        table = parse_table_information(element)

        self.assertEqual("3709F0EB-A274-4A70-8119-7A3D198CC00D", table["id"])
        self.assertEqual("CMN_PRO_Products", table["name"])
        self.assertEqual("This is a COMMENT!", table["comment"])
        self.assertEqual([], table["columns"])

    def test_parse_diagram_information(self):
        element = ET.fromstring(get_resource_content('model/elements/diagram.xml'))
        diagram = parse_diagram_information(element)

        self.assertEqual("1ABE0B5E-152C-48A0-AF62-B865324F28FC", diagram["id"])
        self.assertEqual("Core", diagram["name"])
        self.assertEqual([], diagram["layers"])

    def test_parse_model_information(self):
        element = ET.fromstring(get_resource_content('model/elements/model.xml'))
        model = parse_model_information(element, 'name', 'version')

        self.assertEqual("06355BC2-5C85-4F69-8949-02FCA7E71A1E", model["id"])
        self.assertEqual("name", model["name"])
        self.assertEqual("version", model["version"])
