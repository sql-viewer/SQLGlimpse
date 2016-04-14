from django.db.models import Q
from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sqlviewer.glimpse.models import Version, Table, Diagram, Model
from sqlviewer.glimpse.services import get_diagram_data

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com'


@api_view(["GET"])
def table_details(request, model_id, version_id):
    version = get_object_or_404(Version, pk=version_id, model_id=model_id)
    max_results = max(1, min(int(request.GET.get("size", 0)), 20))
    filters = {"model_version": version}
    if request.GET.get('name'):
        filters["name__contains"] = request.GET['name']

    results = Table.objects.filter(**filters)[:max_results]

    data = [t.to_json(shallow=True) for t in results]
    return Response(data=data, status=status.HTTP_200_OK)


class DiagramView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, model_id, version_id, diagram_id, format=None):
        if not diagram_id:
            diagram_list = get_list_or_404(Diagram, model_version__id=version_id)
            data = [d.to_json() for d in diagram_list]
        else:
            diagram = get_object_or_404(Diagram, id=diagram_id)
            data = get_diagram_data(diagram)

        return Response(data=data, status=status.HTTP_200_OK)


class VersionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, model_id, version_id, format=None):
        if not version_id:
            version_list = get_list_or_404(Version, model__id=model_id)
            data = [v.to_json() for v in version_list]
        else:
            version = get_object_or_404(Version, model_id=model_id, pk=version_id)
            data = version.to_json()
        return Response(data=data, status=status.HTTP_200_OK)


class ModelView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None, model_id=None):
        if not model_id:
            model_list = Model.objects.all()
            data = [m.to_json(shallow=True) for m in model_list]
        else:
            model = get_object_or_404(Model, id=model_id)
            data = model.to_json(shallow=False)
        return Response(data=data, status=status.HTTP_200_OK)
