import hashlib

from rest_framework import serializers
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

from paste.models import Source, Lang
from pastebot.models import BotUser


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('source_name', 'source_source', 'source_lang','source_alias', 'source_bot', 'source_time')

    source_lang = serializers.CharField(read_only=True)
    source_alias = serializers.CharField(read_only=True)
    source_bot = serializers.BooleanField(read_only=True)
    source_time = serializers.DateTimeField(read_only=True)

    # source_bot_user = BotUserSerializer()

    def create(self, validated_data):
        try:
            lang = guess_lexer(validated_data['source_source']).name
        except ClassNotFound:
            lang = 'undefined'

        source = Source(
            source_name=validated_data['source_name'],
            source_source=validated_data['source_source'],
            source_lang=lang
        )
        source.save()

        source.source_alias = hashlib.md5(str(source.id).encode()).hexdigest()[:8]
        source.save()

        return source


class LangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lang
        fields = '__all__'
