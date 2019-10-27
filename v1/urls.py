from django.urls import path

from v1.views import SourceView, LangView


v1 = [
    path('sources/<slug:slug>/', SourceView.as_view()),
    path('sources/', SourceView.as_view()),
    path('languages/<int:pk>/', LangView.as_view()),
    path('languages/', LangView.as_view())
]
