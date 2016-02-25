import copy
import json
from os.path import dirname, join

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


def get_diagram_data(model_id, diagram_id):
    pass
