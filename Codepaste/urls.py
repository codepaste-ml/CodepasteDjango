from django.contrib import admin
from django.urls import path, include

from paste.views import view404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paste.urls.urls')),
    path('', include('bot_adapter.urls')),
    path('', include('social_django.urls', namespace='social'))
]

handler404 = view404
