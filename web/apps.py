# web/apps.py
from django.apps import AppConfig


class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'
    path = '/workspace/web'

    