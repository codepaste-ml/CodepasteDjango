import hashlib
import json

from django.db import Error
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Paste, Language


def index(request):
    return render(request, 'paste.html')


def view404(request, exception, template_name='404.html'):
    return redirect('index')


@csrf_exempt
def post_creation(request):
    source = request.POST.get('source', None)
    name = request.POST.get('name', None)
    language = request.POST.get('language', None)

    _source = Paste(
        source=source,
        name=name,
        language=language
    )

    success = True
    try:
        _source.save()

        _source.alias = hashlib.md5(str(_source.id).encode()).hexdigest()[:8]
        _source.save()
    except Error as e:
        success = False
        print(e)

    data = {
        "success": success,
        "id": _source.alias,
    }

    return JsonResponse(data)


def get_lang(request):
    data = list(map(model_to_dict, Language.objects.all()))

    return JsonResponse({'data': data})


def view_source(request, alias):
    source = get_object_or_404(Paste, alias=alias)
    source = model_to_dict(source, fields="alias, language, name, source, created_using_bot")
    return render(request, 'view.html', {
        'source': json.dumps(json.dumps(source)),
        'alias': alias
    })


def view_source_raw(request, alias):
    source = get_object_or_404(Paste, alias=alias)
    return HttpResponse(source.source, content_type='text/plain')
