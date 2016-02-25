import copy
import json
from os.path import dirname, join
from sqlviewer.viewer.models import Model, Table, Column

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'

with open(join(dirname(__file__), 'resources/model.json')) as fin:
    data = json.load(fin)

models = {
    data["model"]["id"]: data["model"]
}


def get_diagrams_for_model(model_id):
    if model_id in models:
        return models[model_id]["diagrams"]
    else:
        return None


def get_diagram_details(model_id, diagram_id):
    diagrams = get_diagrams_for_model(model_id)
    for dia in diagrams:
        if dia['id'].lower() == diagram_id.lower():
            diagram = copy.deepcopy(dia)
            tbids = []
            for layer in diagram['layers']:
                for table in layer['tables']:
                    tbids.append(table['id'])

            fkids = [c['foreignKeyId'] for c in diagram['connections']]

            return diagram
    return None


def save_model(model):
    """
    Model imported from one of our importers
    :type model: dict
    :return:
    """
    dbmodel = Model.objects.create(
        id=model['id'],
        name=model['name'],
        version=model['version']
    )

    tables = []
    for table in model['data']['tables']:
        dbtable = Table.objects.create(
            id=table['id'],
            name=table['name'],
            comment=table['comment'],
            model=dbmodel
        )
        tables.append(dbtable)

        for col in table['columns']:
            Column.objects.create(
                id=col['id'],
                name=col['name'],
                comment=col['comment'],
                table=dbtable,
                is_key=col['flags']['key'],
                is_auto_increment=col['flags']['autoIncrement'],
                is_nullable=col['flags']['nullable'],
                is_reference=col['flags']['reference'],
                is_hidden=col['flags']['hidden'],
            )
