from django.urls import re_path

from paste.views import view404, view_source_raw

urlpatterns = [
    re_path(r'^(?P<alias>[a-f0-9]{8})/$', view_source_raw, name='view_source_raw'),
]

handler404 = view404
