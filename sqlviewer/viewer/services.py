from sqlviewer.viewer.models import Diagram

__author__ = 'smartinov'


def get_diagrams_for_model(model_id):
    return [
        Diagram("1", "commons"),
        Diagram("2", "healthcare"),
        Diagram("3", "logistics")
    ]


def get_diagram_details(model_id, diagram_id):
    pass
