from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()

v1 = [
    path('', include(router.urls)),
]
