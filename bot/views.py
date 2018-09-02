import json

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from .apps import BotConfig


@csrf_exempt
def webhook(request, token):
    bot = BotConfig.registry.get_bot(token)
    if bot is not None:
        bot.webhook(Update.de_json(json.loads(request.body.decode('utf-8')), bot.bot))
        return HttpResponse()
    else:
        raise Http404
