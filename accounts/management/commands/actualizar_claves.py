from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

SEED_USERS = (
    ('maria.gonzalez@email.com', 'facu2026', {
        'email': 'maria.gonzalez@email.com',
        'display_name': 'María González',
        'account_type': User.AccountType.DONANTE,
    }),
    ('inti@comunidad.org', 'facu2026', {
        'email': 'inti@comunidad.org',
        'display_name': 'inti',
        'account_type': User.AccountType.COMUNIDAD,
    }),
    ('admin@comunidades.org', 'admin2026', {
        'email': 'admin@comunidades.org',
        'display_name': 'Administrador',
        'is_staff': True,
        'is_superuser': True,
    }),
)


class Command(BaseCommand):
    help = 'Restablece las claves de los usuarios iniciales'

    def handle(self, *args, **options):
        for username, password, defaults in SEED_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults=defaults,
            )
            if not created:
                for field, value in defaults.items():
                    setattr(user, field, value)
            user.set_password(password)
            user.save()
            self.stdout.write(f'Clave actualizada: {username}')

        self.stdout.write(self.style.SUCCESS('Usuarios listos para ingresar.'))
