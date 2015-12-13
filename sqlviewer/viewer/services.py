from sqlviewer.viewer.models import Diagram

__author__ = 'smartinov'

models = {
    "model-id": {
        "diagrams": [
            Diagram("1", "commons"),
            Diagram("2", "healthcare"),
            Diagram("3", "logistics")
        ]
    }
}


def get_diagrams_for_model(model_id):
    if model_id in models:
        return models[model_id]["diagrams"]
    else:
        return None


def get_diagram_details(model_id, diagram_id):
    pass
