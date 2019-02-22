from django.urls import re_path

from .views import webhook

urlpatterns = [
    re_path(r'bot/(?P<token>.+)/', webhook),
]
