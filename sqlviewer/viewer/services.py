import json
from os.path import dirname, join
from sqlviewer.viewer.models import Diagram

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'
with open(join(dirname(dirname(__file__)), 'integration/tests/resources/model/mysqlwb.json')) as fin:
    model = json.load(fin)

models = {
    model["model"]["id"]: model["model"]
}


def get_diagrams_for_model(model_id):
    if model_id in models:
        return models[model_id]["diagrams"]
    else:
        return None


def get_diagram_details(model_id, diagram_id):
    pass
