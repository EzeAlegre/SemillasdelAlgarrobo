from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from tickets.models import Ticket

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea el usuario administrador del sistema'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin@comunidades.org',
                email='admin@comunidades.org',
                password='admin2026',
                display_name='Administrador',
            )
            self.stdout.write(self.style.SUCCESS('Administrador creado.'))
        else:
            self.stdout.write('El administrador ya existe.')

        if not Ticket.objects.exists():
            Ticket.objects.create(
                title='Consulta sobre donación',
                description='Un donante consultó sobre cómo recibir comprobante fiscal.',
                category=Ticket.Category.DONATION,
                priority=Ticket.Priority.MEDIUM,
            )
            Ticket.objects.create(
                title='Verificación de comunidad nueva',
                description='Solicitud de verificación para nueva comunidad en Formosa.',
                category=Ticket.Category.COMMUNITY,
                priority=Ticket.Priority.HIGH,
            )
