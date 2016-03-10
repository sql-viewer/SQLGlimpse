# Create your views here.
from os.path import basename

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_list_or_404, redirect
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sqlviewer.glimpse.models import Model, Diagram, Version
import logging
from sqlviewer.glimpse.services import save_imported_model
from sqlviewer.integration.mysqlwb import import_model


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


class DiagramView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, model_id, version_id, diagram_id, format=None):
        if not diagram_id:
            diagram_list = get_list_or_404(Diagram, model_version__id=version_id)
            data = [d.to_json() for d in diagram_list]
        else:
            data = cache.get(diagram_id)
            if not data:
                diagram = get_object_or_404(Diagram, id=diagram_id)
                data = diagram.to_json()
                cache.set(diagram_id, data)

        return Response(data=data, status=status.HTTP_200_OK)


@require_http_methods(["GET"])
@login_required
def models_list_view(request):
    models = Model.objects.all()
    data = {"models": models}
    return render(request, 'viewer/index.html', data)


@require_http_methods(["GET"])
@login_required
def model_version_details_view(request, model_id, version_id):
    version = get_object_or_404(Version, model__id=model_id, pk=version_id)
    data = {"diagrams": version.diagrams(),
            "version_id": version_id,
            "model_id": model_id}
    return render(request, 'viewer/model.html', data)


@require_http_methods(["GET"])
@login_required
def diagram_details_view(request, model_id, version_id, diagram_id):
    diagram = get_object_or_404(Diagram, id=diagram_id, model_version__id=version_id)
    data = diagram.to_json()
    return render(request, 'viewer/diagram.html', data)


@require_http_methods(["GET", "POST"])
@staff_member_required
def model_upload_view(request):
    """
    Administrator view to upload new document versions to the current documents
    """
    if request.method == "GET":
        return render(request, 'viewer/model-upload.html')
    if request.method == "POST":
        tmpfile = request.FILES.get('files[]')
        path = tmpfile.file.name
        imported_data = import_model(path, basename(path))
        save_imported_model(imported_data['model'])
        return redirect(reverse('home'))
