from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'raw', 'paste.urls.raw', name='raw'),
    host(r'(www)?', settings.ROOT_URLCONF, name='default')
)
