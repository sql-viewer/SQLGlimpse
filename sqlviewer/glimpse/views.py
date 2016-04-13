# Create your views here.
from os.path import basename

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rest_framework.generics import get_object_or_404

from sqlviewer.glimpse.models import Model, Diagram, Version
from sqlviewer.glimpse.services import save_imported_model, version_search, get_diagram_data
from sqlviewer.integration.mysqlwb import import_model


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
            "version": version}
    return render(request, 'viewer/version-details.html', data)


@require_http_methods(["GET"])
@login_required
def diagram_details_view(request, model_id, version_id, diagram_id):
    version = get_object_or_404(Version, model__id=model_id, pk=version_id)
    diagram = get_object_or_404(Diagram, id=diagram_id, model_version=version)
    data = {"diagram": get_diagram_data(diagram),
            "version": version}
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


@require_http_methods(["POST"])
@login_required
def version_search_view(request, model_id, version_id):
    if request.method == "POST":
        version = get_object_or_404(Version, model__id=model_id, pk=version_id)
        query = request.POST.get('query')
        data = {
            'query': query,
            'version': version,
            'results': []
        }
        if query and len(query) > 2:
            results = version_search(version, query)
            data['results'] = results
        else:
            data['message'] = 'The provided query is too short!'

        return render(request, 'search/results.html', data)
