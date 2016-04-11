from django.shortcuts import render


# Create your views here.
def connect_view(request, model_id, version_id):
    data = {

    }

    return render(request, 'connect/search.html', data)
