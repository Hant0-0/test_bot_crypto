from django.contrib import admin

from admin_bot.forms import TelegramUserForm, UserStateForm
from admin_bot.models import Telegram_user, UserState


class Telegram_userAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'phone_number', 'username']
    form = TelegramUserForm


admin.site.register(Telegram_user, Telegram_userAdmin)


class UserStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_state']
    form = UserStateForm


admin.site.register(UserState, UserStateAdmin)

