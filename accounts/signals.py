from django.db.models.signals import post_save
from django.dispatch import receiver

from communities.models import Community

from .models import User


@receiver(post_save, sender=User)
def create_community_profile(sender, instance, created, **kwargs):
    if created and instance.is_community and not hasattr(instance, 'community_profile'):
        Community.objects.create(
            owner=instance,
            name=f'Comunidad de {instance.get_display_name()}',
            description='Comunidad registrada en la plataforma.',
            province=Community.Province.SALTA,
            population=0,
            email=instance.email,
        )
