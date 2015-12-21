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

    for diagram_element in root.findall('.//value[@type="object"][@struct-name="workbench.physical.Diagram"]'):
        diagram = parse_diagram_information(diagram_element)
        model['diagrams'].append(diagram)

        for layer_element in diagram_element.findall(
                './/value[@type="object"][@struct-name="workbench.physical.Layer"]'):
            layer = parse_layer_information(layer_element)
            diagram['layers'].append(layer)

            for table_element in diagram_element.findall(
                    './/value[@type="object"][@struct-name="workbench.physical.TableFigure"]'):
                table_layer_id = table_element.find('.link[@key="layer"]').text.strip('{}')
                if table_layer_id == layer['id']:
                    table = parse_table_figure_information(table_element)
                    layer['tables'].append(table)

    return {'model': model}


def parse_model_information(element, name, version):
    """

    :param element:
    :type element: _elementtree.Element
    :return:
    """
    return {
        'id': element.get('id').strip('{}'),
        'name': name,
        'version': version,
        'diagrams': [],
        'data': {
            'tables': []
        }
    }


def parse_diagram_information(element):
    """

    :param element:
    :type element: _elementtree.Element
    :return:
    """
    return {
        "id": element.get('id').strip('{}'),
        "name": element.find('.value[@key="name"]').text,
        "layers": []
    }


def parse_table_information(element):
    """

    :param element:
    :type element: _elementtree.Element
    :return:
    """
    return {
        "id": element.get('id').strip('{}'),
        "name": element.find('.value[@key="name"]').text,
        "comment": element.find('.value[@key="comment"]').text,
        "columns": []
    }


def parse_table_figure_information(element):
    """

    :param element:
    :type element: _elementtree.Element
    :return:
    """
    return {
        "id": element.get('id').strip('{}'),
        "tableId": element.find('.link[@key="table"]').text.strip('{}'),
        "element": {

            "x": convert_workbench_size(element.find('.value[@key="left"]').text),
            "y": convert_workbench_size(element.find('.value[@key="top"]').text),
            "width": convert_workbench_size(element.find('.value[@key="width"]').text),
            "height": convert_workbench_size(element.find('.value[@key="height"]').text),
            "color": element.find('.value[@key="color"]').text or "#FFFFFF",
            "collapsed": element.find('.value[@key="expanded"]').text == "0"
        }
    }


def parse_layer_information(element):
    """

    :param element:
    :type element: _elementtree.Element
    :return:
    """

    return {
        "id": element.get('id').strip('{}'),
        "name": element.get('key') if 'key' in element.attrib else element.find('.value[@key="name"]').text,
        "description": element.find('.value[@key="description"]').text,
        "element": {
            "x": convert_workbench_size(element.find('.value[@key="left"]').text),
            "y": convert_workbench_size(element.find('.value[@key="top"]').text),
            "width": convert_workbench_size(element.find('.value[@key="width"]').text),
            "height": convert_workbench_size(element.find('.value[@key="height"]').text),
            "color": element.find('.value[@key="color"]').text or "#FFFFFF"
        },
        "tables": []
    }


def parse_column_information(element, table_id, ordinal):
    """

    :param element:
    :type element: _elementtree.Element
    :return:
    """
    column = {
        "id": element.get('id').strip('{}'),
        "tableId": table_id,
        "name": element.find('.value[@key="name"]').text,
        "comment": element.find('.value[@key="comment"]').text,
    }
    flags = {
        "key": False if ordinal else True,
        "nullable": int(element.find('.value[@key="isNotNull"]').text) is 0,
        "autoIncrement": False,
        "hidden": False,
        "reference": column['name'].endswith('_RefID')
    }

    column['flags'] = flags

    return column


def convert_workbench_size(value):
    segments = value.split("e+")
    return int(float(segments[0]) * (10 ** int(segments[1])))


def read_model_from_zip(path):
    zip_file = ZipFile(path)
    return zip_file.read("document.mwb.xml")
