import json
from django.test import TestCase
from os.path import dirname, join
from sqlviewer.glimpse.models import Model, Table, Column, ForeignKey
from django.db.models import Q

from sqlviewer.glimpse.services import save_imported_model

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


class TestViewerServices(TestCase):
    def setUp(self):
        with open(join(dirname(__file__), 'resources/model.json')) as fin:
            data = json.load(fin)
        save_imported_model(data['model'])


    def test_get_diagram_details(self):
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

        foreign_key = ForeignKey.objects.filter(model=model)
        self.assertEqual(11, len(foreign_key))
        pk_references = ForeignKey.objects.filter(Q(source_column=primary_key) | Q(target_column=primary_key))
        self.assertEqual(1, len(pk_references))
        pkref = pk_references.first()
        self.assertEqual("CMN_PRO_Catalog_Products", pkref.source_table.name)
        self.assertEqual("CMN_PRO_Products", pkref.target_table.name)
