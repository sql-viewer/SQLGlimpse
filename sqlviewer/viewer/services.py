from sqlviewer.viewer.models import Diagram

__author__ = 'smartinov'


def get_diagrams(model_id):
    return [
        Diagram(1, "commons"),
        Diagram(2, "healthcare"),
        Diagram(3, "logistics")
    ]
