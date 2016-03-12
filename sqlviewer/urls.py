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
from django.contrib import admin


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout as logout_view
from django.views.static import serve as django_static_serve
from sqlviewer.glimpse.views import diagram_details_view, model_version_details_view, models_list_view, ModelView, VersionView, DiagramView, model_upload_view, \
    version_search_view
from sqlviewer.settings.common import STATIC_ROOT

api = [
    url(r'^api/v1/models/(?P<model_id>\d+)?$', ModelView.as_view()),
    url(r'^api/v1/models/(?P<model_id>\d+)/versions/(?P<version_id>\d+)?$', VersionView.as_view()),
    url(r'^api/v1/models/(?P<model_id>\d+)/versions/(?P<version_id>\d+)/diagrams/(?P<diagram_id>\d+)?$', DiagramView.as_view()),
]
pages = [
    url(r'^$', models_list_view, name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^models/upload$', model_upload_view, name='model_upload'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^models/(?P<model_id>\d+)/versions/(?P<version_id>\d+)$', model_version_details_view, name='model_details'),
    url(r'^models/(?P<model_id>\d+)/versions/(?P<version_id>\d+)/search$', version_search_view, name='version_search'),
    url(r'^models/(?P<model_id>\d+)/versions/(?P<version_id>\d+)/diagrams/(?P<diagram_id>\d+)$', diagram_details_view, name='diagram_details'),
]

heroku_statics = [
    url(r'^static/(?P<path>.*)$', django_static_serve, {'document_root': STATIC_ROOT})
]
# 
urlpatterns = pages + api + heroku_statics
