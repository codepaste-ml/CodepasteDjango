import traceback
import json

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from telegram import Update

from .apps import BotConfig


@csrf_exempt
def bot(request):
    try:
        BotConfig.bot.webhook(Update.de_json(json.loads(request.body.decode('utf-8')), BotConfig.bot.bot))

        return HttpResponse('OK')
    except:
        traceback.print_exc()
        raise Http404
