from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from paste.models import Source, Lang
from v1.serializers import SourceSerializer, LangSerializer


class SourceView(APIView):
    def get(self, _, slug=None):
        if slug is None:
            return Response(status.HTTP_400_BAD_REQUEST)

        source = get_object_or_404(Source, source_alias=slug)
        return Response(SourceSerializer(source).data, status=status.HTTP_200_OK)

    def post(self, request):
        source = SourceSerializer(data=request.data)
        source.is_valid(raise_exception=True)
        source.save()

        return Response(source.data)


class LangView(APIView):
    def get(self, _, pk=None):
        if pk is None:
            return Response(LangSerializer(Lang.objects.all(), many=True).data)

        lang = get_object_or_404(Lang, pk=pk)
        return Response(LangSerializer(lang).data, status=status.HTTP_200_OK)