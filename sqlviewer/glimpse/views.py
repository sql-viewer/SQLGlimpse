# Create your views here.
from django.http.response import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from sqlviewer.glimpse.models import Model, Diagram, Version


class ModelView(APIView):
    def get(self, request, format=None, model_id=None):
        if not model_id:
            models = Model.objects.all()
            data = [m.to_json(shallow=True) for m in models]
        else:
            model = get_object_or_404(Model, id=model_id)
            data = [d.to_json(shallow=True) for d in model.diagrams()]
        return Response(data=data, status=status.HTTP_200_OK)


class VersionView(APIView):
    def get(self, request, model_id, version_id, format=None):
        if version_id:
            version = get_object_or_404(Version, model_id=model_id, pk=version_id)
        else:
            pass


class DiagramsView(APIView):
    pass


@api_view(["GET"])
def diagram_list_api_view(request, model_id):
    model = get_object_or_404(Model, id=model_id)
    data = [d.to_json(shallow=True) for d in model.diagrams()]
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
def diagram_details_api_view(request, model_id, diagram_id):
    diagram = get_object_or_404(Diagram, id=diagram_id, model__id=model_id)
    data = diagram.to_json()
    return Response(data=data, status=status.HTTP_200_OK)


@require_http_methods(["GET"])
def models_list_view(request):
    models = Model.objects.all()
    data = {"models": models}
    return render(request, 'viewer/index.html', data)


@require_http_methods(["GET"])
def model_details_view(request, model_id):
    model = get_object_or_404(Model, id=model_id)
    data = {"diagrams": model.diagrams(),
            "model_id": model_id}
    return render(request, 'viewer/model.html', data)


@require_http_methods(["GET"])
def diagram_details_view(request, model_id, diagram_id):
    diagram = get_object_or_404(Diagram, id=diagram_id, model__id=model_id)
    data = diagram.to_json()
    return render(request, 'viewer/diagram.html', data)
