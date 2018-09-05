"""Codepaste URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from paste.views import index, post_creation, get_lang, view_source

urlpatterns = [
    path('ajax/createPost/', post_creation, name='post_creation'),
    path('ajax/getLang/', get_lang, name='get_lang'),
    re_path(r'^(?P<alias>[a-f0-9]{8})/$', view_source, name='view_source'),
    path('', index, name='index'),
]
