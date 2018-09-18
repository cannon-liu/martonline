from django.apps import AppConfig

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
User = get_user_model()


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = "用户管理"

    def ready(self):

        from .signals import create_auth_token
        post_save.connect(
            receiver=create_auth_token,
            sender=User
        )
