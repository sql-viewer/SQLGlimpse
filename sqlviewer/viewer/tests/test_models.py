import json
import os
from django.test import TestCase
from sqlviewer.viewer.models import Column, Table, ForeignKey, TableElement, LayerElement, ConnectionElement, Diagram
from sqlviewer.viewer.services import save_imported_model


class ModelSerializationTest(TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'resources/model-small.json')) as fin:
            data = json.load(fin)
        save_imported_model(data['model'])

    def test_column_serialization(self):
        column = Column.objects.get(id='70A39AC0-1194-4831-94B2-B663A2118C42')

        data = column.to_json()
        self.assertEqual("70A39AC0-1194-4831-94B2-B663A2118C42".lower(), data['id'])
        self.assertEqual("CMN_PRO_ProductID", data['name'])
        self.assertEqual(None, data['comment'])
        self.assertEqual(True, data['flags']['key'])
        self.assertEqual(False, data['flags']['autoIncrement'])
        self.assertEqual(False, data['flags']['reference'])
        self.assertEqual(False, data['flags']['hidden'])

    def test_table_serialization(self):
        table = Table.objects.get(id='6a2c07b6-8dad-4ff9-b5e7-85c3e34c136d')

        data = table.to_json()
        self.assertEqual('6a2c07b6-8dad-4ff9-b5e7-85c3e34c136d', data['id'])
        self.assertEqual('CMN_PRO_Catalog_Products', data['name'])
        self.assertEqual(None, data['comment'])
        self.assertEqual(3, len(data['columns']))

    def test_foreign_key_serialization(self):
        fk = ForeignKey.objects.get(id='50509361-E961-41DC-A7CB-E9267D4238C4')

        data = fk.to_json()
        self.assertEqual('50509361-e961-41dc-a7cb-e9267d4238c4', data['id'])
        self.assertEqual('column', data['type'])
        self.assertEqual("6A2C07B6-8DAD-4FF9-B5E7-85C3E34C136D".lower(), data['source']['tableId'])
        self.assertEqual("C9AC6FCD-3B74-458C-B551-3C62AAAC42E8".lower(), data['source']['columnId'])
        self.assertEqual("3709F0EB-A274-4A70-8119-7A3D198CC00D".lower(), data['target']['tableId'])
        self.assertEqual("70A39AC0-1194-4831-94B2-B663A2118C42".lower(), data['target']['columnId'])

    def test_table_element_serialization(self):
        table_element = TableElement.objects.get(id='CA8DEB78-99DD-4EB3-9F40-DDE75431D7BB')

        data = table_element.to_json()
        self.assertEqual('CA8DEB78-99DD-4EB3-9F40-DDE75431D7BB'.lower(), data['id'])
        self.assertEqual('3709F0EB-A274-4A70-8119-7A3D198CC00D'.lower(), data['tableId'])
        self.assertEqual(False, data['element']['collapsed'])
        self.assertEqual('#98BFDA', data['element']['color'])
        self.assertEqual(190, data['element']['height'])
        self.assertEqual(330, data['element']['width'])
        self.assertEqual(87, data['element']['x'])
        self.assertEqual(37, data['element']['y'])

    def test_layer_element_serialization(self):
        layer_element = LayerElement.objects.get(id='58A8526D-4C44-4896-A18E-EDBFFC7E7E4A')

        data = layer_element.to_json()
        self.assertEqual('58A8526D-4C44-4896-A18E-EDBFFC7E7E4A'.lower(), data['id'])
        self.assertEqual('LayerName', data['name'])
        self.assertEqual(None, data['description'])
        self.assertEqual('#F0F1FE', data['element']['color'])
        self.assertEqual(300, data['element']['height'])
        self.assertEqual(512, data['element']['width'])
        self.assertEqual(641, data['element']['x'])
        self.assertEqual(943, data['element']['y'])
        self.assertEqual(1, len(data['tables']))

    def test_connection_element_serialization(self):
        connection_element = ConnectionElement.objects.get(id='2AC90AD8-4D61-47E8-A274-3D840C65558B')

        data = connection_element.to_json()
        self.assertEqual('2AC90AD8-4D61-47E8-A274-3D840C65558B'.lower(), data['id'])
        self.assertEqual('50509361-E961-41DC-A7CB-E9267D4238C4'.lower(), data['foreignKeyId'])
        self.assertEqual('full', data['element']['draw'])

    def test_diagram_element_serialization(self):
        diagram_element = Diagram.objects.get(id="1ABE0B5E-152C-48A0-AF62-B865324F28FC")

        data = diagram_element.to_json()
        self.assertEqual('1ABE0B5E-152C-48A0-AF62-B865324F28FC'.lower(), data['id'])
        self.assertEqual('Core', data['name'])
        self.assertEqual(2, len(data['layers']))
        self.assertEqual(1, len(data['connections']))
        self.assertEqual(2, len(data['data']['tables']))
        self.assertEqual(1, len(data['data']['foreignKeys']))

        data = diagram_element.to_json(shallow=True)
        self.assertFalse('layers' in data)
        self.assertFalse('connections' in data)
        self.assertFalse('data' in data)
