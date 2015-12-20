from zipfile import ZipFile
from xml.etree import ElementTree as ET

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


def import_model(model_path, name, version):
    content = read_model_from_zip(model_path)
    root = ET.ElementTree(ET.fromstring(content))

    data = parse_model_information(root, name, version)

    return data


def parse_model_information(root, name, version):
    model_element = root.find('.//value[@struct-name="workbench.logical.Model"]')
    model = {
        'id': model_element.get('id').strip('{}'),
        'name': name,
        'version': version
    }
    return {'model': model}


def read_model_from_zip(path):
    zip_file = ZipFile(path)
    return zip_file.read("document.mwb.xml")
