from django.conf.urls import url
from core import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^refresh/$', views.refresh, name='refresh'),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]