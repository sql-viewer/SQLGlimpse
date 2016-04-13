from django.shortcuts import render, get_object_or_404


# Create your views here.
from sqlviewer.glimpse.models import Version


def connect_view(request, model_id, version_id):
    version = get_object_or_404(Version, model__id=model_id, pk=version_id)
    data = {"version": version}

    return render(request, 'connect/search.html', data)
