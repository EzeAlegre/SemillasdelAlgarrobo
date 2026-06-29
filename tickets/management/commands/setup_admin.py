from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Alias de crear_admin (comando anterior)'

    def handle(self, *args, **options):
        call_command('crear_admin')
