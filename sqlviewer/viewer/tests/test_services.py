import json
from django.test import TestCase
from os.path import dirname, join
from sqlviewer.viewer.models import Model, Table, Column

from sqlviewer.viewer.services import save_model

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


class TestViewerServices(TestCase):
    def test_get_diagram_details(self):
        with open(join(dirname(dirname(__file__)), 'resources/model.json')) as fin:
            data = json.load(fin)

        save_model(data['model'])
        model = Model.objects.get(id='EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6')
        self.assertEqual('name', model.name)
        self.assertEqual('version', model.version)

        tables = Table.objects.filter(model=model)
        self.assertEqual(9, len(tables))

        product_table = Table.objects.filter(model=model, name='CMN_PRO_Products').first()
        self.assertEqual(6, len(product_table.columns()))
        primary_key = Column.objects.get(table=product_table, is_key=True)
        self.assertEqual('70A39AC0-1194-4831-94B2-B663A2118C42', str(primary_key.id).upper())
        self.assertEqual(None, primary_key.comment)
        self.assertEqual('CMN_PRO_ProductID', primary_key.name)
