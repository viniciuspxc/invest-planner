"""
AppConfig File
"""
from django.apps import AppConfig


class BaseConfig(AppConfig):
    """
    AppConfig for base module
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
