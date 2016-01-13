# Create your views here.
from django.http.response import HttpResponse, Http404, HttpResponseNotAllowed
import json
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from django.shortcuts import render

from sqlviewer.viewer.services import get_diagrams_for_model
from sqlviewer.viewer.services import get_diagram_details


@api_view(["GET"])
def diagram_list_api_view(request, model_id):
    diagrams = get_diagrams_for_model(model_id)
    if diagrams:
        return Response(data=diagrams, status=status.HTTP_200_OK)
    else:
        raise Http404("Model not found")

@api_view(["GET"])
def diagram_details_api_view(request, model_id, diagram_id):
    diagrams = get_diagrams_for_model(model_id)
    if diagrams:
        return Response(data=diagrams, status=status.HTTP_200_OK)
    else:
        raise Http404("Model not found")

def model_details_view(request, model_id):
    if request.method == "GET":
        diagrams = get_diagrams_for_model(model_id)
        if diagrams:
            data = {"diagrams": diagrams,
                    "model_id": model_id}
            return render(request, 'viewer/model.html', data)
        else:
            raise Http404("Model not found")
    else:
        raise HttpResponseNotAllowed(['GET'])


def diagram_details_view(request, model_id, diagram_id):
    diagram = get_diagram_details(model_id, diagram_id)
    data = {"diagram": diagram,
            "model_id": model_id}
    return render(request, 'viewer/diagram.html', data)
