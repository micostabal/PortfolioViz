from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_mymodel_instances(sender, **kwargs):
    pass