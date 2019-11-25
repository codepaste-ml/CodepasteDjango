import hashlib

from rest_framework import serializers
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

from paste.models import Paste, Language
from pastebot.models import BotUser


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paste
        fields = ('name', 'source', 'language', 'alias', 'created_using_bot', 'creation_date')

    language = serializers.CharField(read_only=True)
    alias = serializers.CharField(read_only=True)
    created_using_bot = serializers.BooleanField(read_only=True)
    creation_date = serializers.DateTimeField(read_only=True)

    # source_bot_user = BotUserSerializer()

    def create(self, validated_data):
        try:
            language = guess_lexer(validated_data['source']).name
        except ClassNotFound:
            language = 'undefined'

        source = Paste(
            name=validated_data['name'],
            source=validated_data['source'],
            language=language
        )
        source.save()

        source.alias = hashlib.md5(str(source.id).encode()).hexdigest()[:8]
        source.save()

        return source


class LangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
