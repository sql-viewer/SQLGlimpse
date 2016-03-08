# Create your views here.
from django.http.response import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, get_list_or_404
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
            model_list = Model.objects.all()
            data = [m.to_json(shallow=True) for m in model_list]
        else:
            model = get_object_or_404(Model, id=model_id)
            data = model.to_json(shallow=False)
        return Response(data=data, status=status.HTTP_200_OK)


class VersionView(APIView):
    def get(self, request, model_id, version_id, format=None):
        if not version_id:
            version_list = get_list_or_404(Version, model__id=model_id)
            data = [v.to_json() for v in version_list]
        else:
            version = get_object_or_404(Version, model_id=model_id, pk=version_id)
            data = version.to_json()
        return Response(data=data, status=status.HTTP_200_OK)


class DiagramView(APIView):
    def get(self, request, model_id, version_id, diagram_id, format=None):
        if not diagram_id:
            diagram_list = get_list_or_404(Diagram, model_version__id=version_id)
            data = [d.to_json() for d in diagram_list]
        else:
            diagram = get_object_or_404(Diagram, id=diagram_id)
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
