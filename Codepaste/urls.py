from django.contrib import admin
from django.urls import path, include

from v1.urls import v1
from paste.views import view404


urlpatterns = [
    path('api/', include(v1)),
    path('api/v1/', include(v1)),

    path('admin/', admin.site.urls),

    path('', include('paste.urls.urls')),
    path('', include('bot_adapter.urls')),
]

handler404 = view404
