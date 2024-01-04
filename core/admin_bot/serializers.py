from rest_framework import serializers

from admin_bot.models import Telegram_user, UserState


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram_user
        fields = '__all__'


class UserStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserState
        fields = '__all__'
