import hashlib
import json

from django.db import Error
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Source, Lang


def index(request):
    return render(request, 'paste.html')


def view404(request, exception, template_name='404.html'):
    return redirect('/')


def post_creation(request):
    source = request.POST.get('source', None)
    name = request.POST.get('name', None)
    lang = request.POST.get('lang', None)

    _source = Source(
        source_source=source,
        source_name=name,
        source_lang=lang
    )

    success = True
    try:
        _source.save()

        _source.source_alias = hashlib.md5(str(_source.id).encode()).hexdigest()[:8]
        _source.save()
    except Error as e:
        success = False
        print(e)

    data = {
        "success": success,
        "id": _source.source_alias,
    }

    return JsonResponse(data)


def get_lang(request):
    data = list(map(model_to_dict, Lang.objects.all()))

    return JsonResponse({'data': data})


def view_source(request, alias):
    source = get_object_or_404(Source, source_alias=alias)
    source = model_to_dict(source, fields="source_alias, source_lang, source_name, source_source, source_bot")

    return render(request, 'view.html', {'source': json.dumps(json.dumps(source))})
