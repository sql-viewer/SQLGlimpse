import json
from django.test import TestCase
from os.path import dirname, join
from sqlviewer.glimpse.models import Model, Table, Column, ForeignKey, Version
from django.db.models import Q

from sqlviewer.glimpse.services import save_imported_model, version_search

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


class TestViewerServices(TestCase):
    def setUp(self):
        with open(join(dirname(__file__), 'resources/model.json')) as fin:
            self.model_data = json.load(fin)['model']
        save_imported_model(self.model_data)

    def test_search_service(self):
        version = Version.objects.first()
        results = version_search(version, 'Product')
        self.assertEqual(1, len(results))
        self.assertDictEqual({
            "type": "table",
            "name": "CMN_PRO_Products",
            "diagram": {
                "id": 1,
                "name": "Core"
            },
            "layer": {
                "id": "dfa75dce-dbd1-4c45-87ff-5891f71648dd",
                "color": "#FFFFFF",
                "name": "rootLayer"
            }

        }, results[0])

    def test_save_multiple_model_versions(self):
        model = Model.objects.get(extid='EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6')
        version = model.latest_version()

        self.assertEqual(0, version.number)
        self.assertEqual('version', version.label)

        self.model_data['version'] = 'new version'
        save_imported_model(self.model_data)
        version = model.latest_version()
        self.assertEqual(1, version.number)
        self.assertEqual('new version', version.label)

    def test_get_diagram_details(self):
        model = Model.objects.get(extid='EBDB3E5E-7DC4-4BC9-9D35-C9A75372A8E6')
        self.assertEqual('name', model.name)

        version = model.latest_version()

        tables = Table.objects.filter(model_version=version)
        self.assertEqual(9, len(tables))

        product_table = Table.objects.filter(model_version=version, name='CMN_PRO_Products').first()
        self.assertEqual(6, len(product_table.columns()))
        primary_key = Column.objects.get(table=product_table, is_key=True)
        self.assertEqual('70A39AC0-1194-4831-94B2-B663A2118C42', str(primary_key.extid).upper())
        self.assertEqual(None, primary_key.comment)
        self.assertEqual('CMN_PRO_ProductID', primary_key.name)

        foreign_key = ForeignKey.objects.filter(model_version=version)
        self.assertEqual(11, len(foreign_key))
        pk_references = ForeignKey.objects.filter(Q(source_column=primary_key) | Q(target_column=primary_key))
        self.assertEqual(1, len(pk_references))
        pkref = pk_references.first()
        self.assertEqual("CMN_PRO_Catalog_Products", pkref.source_table.name)
        self.assertEqual("CMN_PRO_Products", pkref.target_table.name)
