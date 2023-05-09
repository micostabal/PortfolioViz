from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PortfolioVizConfig(AppConfig):
    name = 'portfolioviz'
    
    def ready(self):
        pass
