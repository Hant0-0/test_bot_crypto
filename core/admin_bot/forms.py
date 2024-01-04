from django import forms

from admin_bot.models import Telegram_user, UserState


class TelegramUserForm(forms.ModelForm):
    class Meta:
        model = Telegram_user
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'username',
            'user_id',
        ]


class UserStateForm(forms.ModelForm):
    class Meta:
        model = UserState
        fields = [
            'user',
            'current_state',
        ]