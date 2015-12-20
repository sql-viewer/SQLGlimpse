from zipfile import ZipFile
from xml.etree import ElementTree as ET

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


def import_model(model_path, name, version):
    content = read_model_from_zip(model_path)
    root = ET.ElementTree(ET.fromstring(content))

    model_element = root.find('.//value[@struct-name="workbench.logical.Model"]')
    model = parse_model_information(model_element, name, version)

    for table_element in root.findall('.//value[@type="object"][@struct-name="db.mysql.Table"]'):
        table = parse_table_information(table_element)
        model['data']['tables'].append(table)

        query = '.value[@key="columns"]/value[@struct-name="db.mysql.Column"]'
        for idx, column_element in enumerate(table_element.findall(query)):
            column = parse_column_information(column_element, table['id'], idx)
            table['columns'].append(column)

    return {"model": model}


def parse_model_information(model_element, name, version):
    return {
        'id': model_element.get('id').strip('{}'),
        'name': name,
        'version': version,
        'diagrams': [],
        'data': {
            'tables': []
        }
    }


def parse_table_information(table_element):
    return {
        "id": table_element.get('id').strip('{}'),
        "name": table_element.find('.value[@key="name"]').text,
        "comment": table_element.find('.value[@key="comment"]').text,
        "columns": []
    }


def parse_column_information(column_element, table_id, ordinal):
    column = {
        "id": column_element.get('id').strip('{}'),
        "tableId": table_id,
        "name": column_element.find('.value[@key="name"]').text,
        "comment": column_element.find('.value[@key="comment"]').text,
    }
    flags = {
        "key": False if ordinal else True,
        "nullable": int(column_element.find('.value[@key="isNotNull"]').text) is 0,
        "autoIncrement": False,
        "hidden": False,
        "reference": column['name'].endswith('_RefID')
    }

    column['flags'] = flags

    return column


def read_model_from_zip(path):
    zip_file = ZipFile(path)
    return zip_file.read("document.mwb.xml")
