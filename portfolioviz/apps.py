from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PortfolioVizConfig(AppConfig):
    name = 'portfolioviz'
    
    def ready(self):
        pass
        # from portfolioviz.signals import create_mymodel_instances
        # post_migrate.connect(create_mymodel_instances)
