# Create your views here.
import jsonpickle as jsonpickle

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render_to_response, render

from sqlviewer.viewer.services import get_diagrams


class DiagramsView(APIView):
    def get(self, request, *args, **kw):
        diagrams = get_diagrams(1)
        data = jsonpickle.dumps(diagrams)
        response = Response(data=data, status=status.HTTP_200_OK)
        return response


def home(request):
    return render(request, 'viewer/index.html')
