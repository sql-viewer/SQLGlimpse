# Create your views here.
from django.http.response import HttpResponse, Http404, HttpResponseNotAllowed
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from django.shortcuts import render
from sqlviewer.viewer.models import Model


@api_view(["GET"])
def diagram_list_api_view(request, model_id):
    model = get_object_or_404(Model, id=model_id)

    diagrams = []
    for dia in model.diagrams():
        diagrams.append(
            {
                "id": dia.id,
                "name": dia.name
            }
        )

    return Response(data=diagrams, status=status.HTTP_200_OK)


@api_view(["GET"])
def diagram_details_api_view(request, model_id, diagram_id):
    pass


@api_view(["GET"])
def model_details_view(request, model_id):
    if request.method == "GET":
        pass
    else:
        raise HttpResponseNotAllowed(['GET'])


@api_view(["GET"])
def diagram_details_view(request, model_id, diagram_id):
    pass
