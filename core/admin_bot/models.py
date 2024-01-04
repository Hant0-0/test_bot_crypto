from django.db import models


class Telegram_user(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    user_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.username}"


class UserState(models.Model):
    user = models.OneToOneField(Telegram_user, on_delete=models.CASCADE)
    current_state = models.CharField(max_length=100, default='initial')

    def __str__(self):
        return f"{self.user} ----- {self.current_state}"
