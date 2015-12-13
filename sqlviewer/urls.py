"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from django.views.generic import RedirectView
import sqlviewer
from sqlviewer.viewer.views import DiagramsView

urlpatterns = [
    url(r'^api/v1/models/(?P<model_id>\w+)/diagrams/(?P<diagram_id>\w+)[/]?$',
        DiagramsView.as_view(), name='diagrams_view'),
    url(r'^api/v1/models/(?P<model_id>\w+)/diagrams[/]?$',
        DiagramsView.as_view(), name='diagrams_view'),

    url(r'^$', RedirectView.as_view(url='/home')),
    url(r'^home$', sqlviewer.viewer.views.home, name='home')
]
