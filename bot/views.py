import json

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from .apps import BotConfig


@csrf_exempt
def webhook(request, token):
    print("Catched webhook with token %s" % token)
    bot = BotConfig.registry.get_bot(token)
    print("Get bot")
    if bot is not None:
        print("Bot is not None")
        bot.webhook(Update.de_json(json.loads(request.body.decode('utf-8')), bot.bot))
        print("Passed updated")
        return HttpResponse()
    else:
        raise Http404
