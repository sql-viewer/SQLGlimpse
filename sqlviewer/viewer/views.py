# Create your views here.
import jsonpickle as jsonpickle

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render_to_response, render

from sqlviewer.viewer.services import get_diagrams_for_model
from viewer.services import get_diagram_details


class DiagramsView(APIView):
    def get(self, request, *args, **kw):
        diagrams = get_diagrams_for_model(1)
        data = jsonpickle.dumps(diagrams)
        response = Response(data=data, status=status.HTTP_200_OK)
        return response


def model_view(request, model_id):
    diagrams = get_diagrams_for_model(model_id)
    data = {"diagrams": diagrams,
            "model_id": model_id}
    return render(request, 'viewer/model.html', data)


def diagram_view(request, model_id, diagram_id):
    diagram = get_diagram_details(model_id, diagram_id)
    data = {"diagram": diagram,
            "model_id": model_id}
    return render(request, 'viewer/diagram.html', data)
