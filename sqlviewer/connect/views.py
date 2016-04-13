from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.views.decorators.http import require_http_methods
from sqlviewer.connect.services import connect_tables
from sqlviewer.glimpse.models import Version


@require_http_methods(["GET"])
@login_required
def connect_view(request, model_id, version_id):
    version = get_object_or_404(Version, model__id=model_id, pk=version_id)

    if request.GET.get('from') and request.GET.get('to'):
        source_table = request.GET.get('from')
        target_table = request.GET.get('to')
        results = connect_tables(version, source_table, target_table)
    else:
        results = []
    print(results)
    data = {"version": version,
            "results": results}

    return render(request, 'connect/search.html', data)
