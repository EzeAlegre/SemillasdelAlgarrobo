from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from communities.models import Community, Donation, Need

User = get_user_model()


class Command(BaseCommand):
    help = 'Carga datos iniciales del sistema'

    def handle(self, *args, **options):
        if Community.objects.filter(name='Comunidad Wichí La Esperanza').exists():
            self.stdout.write('Los datos iniciales ya están cargados.')
            return

        donante, _ = User.objects.get_or_create(
            username='maria.gonzalez@email.com',
            defaults={
                'email': 'maria.gonzalez@email.com',
                'display_name': 'María González',
                'account_type': User.AccountType.DONANTE,
            },
        )
        donante.set_password('facu2026')
        donante.save()

        community_user, _ = User.objects.get_or_create(
            username='inti@comunidad.org',
            defaults={
                'email': 'inti@comunidad.org',
                'display_name': 'inti',
                'account_type': User.AccountType.COMUNIDAD,
            },
        )
        community_user.set_password('facu2026')
        community_user.save()

        Community.objects.filter(owner=community_user).delete()

        communities_data = [
            {
                'name': 'Comunidad Wichí La Esperanza',
                'description': 'Comunidad de 250 familias dedicadas a la agricultura tradicional y artesanías.',
                'province': Community.Province.SALTA,
                'population': 1200,
                'email': 'la.esperanza@email.com',
                'image_url': '/static/img/comunidad-default.svg',
                'owner': community_user,
                'needs': [
                    {
                        'title': 'Alimentos no perecederos para el invierno',
                        'description': 'Necesitamos alimentos no perecederos para 250 familias durante el invierno. Prioridad: arroz, fideos, aceite, azúcar y harina.',
                        'category': Need.Category.ALIMENTOS,
                        'target_amount': Decimal('150000'),
                        'is_urgent': True,
                        'raised': Decimal('87500'),
                    },
                    {
                        'title': 'Botiquín médico comunitario',
                        'description': 'Equipamiento médico básico y medicamentos para atención primaria de salud.',
                        'category': Need.Category.SALUD,
                        'target_amount': Decimal('80000'),
                        'is_urgent': False,
                        'raised': Decimal('45000'),
                    },
                ],
            },
            {
                'name': 'Pueblo Guaraní Yvy Maraey',
                'description': 'Pueblo ancestral dedicado a la preservación de sus tradiciones y el cultivo de la tierra.',
                'province': Community.Province.JUJUY,
                'population': 800,
                'email': 'yvy.maraey@email.com',
                'image_url': '/static/img/comunidad-default.svg',
                'needs': [
                    {
                        'title': 'Semillas nativas para la próxima cosecha',
                        'description': 'Semillas de maíz, poroto y zapallo para garantizar la producción alimentaria del pueblo.',
                        'category': Need.Category.ALIMENTOS,
                        'target_amount': Decimal('60000'),
                        'is_urgent': False,
                        'raised': Decimal('22000'),
                    },
                ],
            },
            {
                'name': 'Comunidad Qom Namagoik',
                'description': 'Comunidad trabajando en proyectos de educación bilingüe y desarrollo sostenible.',
                'province': Community.Province.CHACO,
                'population': 650,
                'email': 'namagoik@email.com',
                'image_url': '/static/img/comunidad-default.svg',
                'needs': [
                    {
                        'title': 'Material escolar bilingüe',
                        'description': 'Libros, cuadernos y materiales didácticos en qom y castellano para la escuela comunitaria.',
                        'category': Need.Category.EDUCACION,
                        'target_amount': Decimal('45000'),
                        'is_urgent': True,
                        'raised': Decimal('12000'),
                    },
                ],
            },
        ]

        for data in communities_data:
            needs_data = data.pop('needs')
            owner = data.pop('owner', None)
            community = Community.objects.create(owner=owner, **data)
            for need_data in needs_data:
                raised = need_data.pop('raised')
                need = Need.objects.create(community=community, **need_data)
                if raised > 0:
                    Donation.objects.create(
                        need=need,
                        donor=donante,
                        amount=raised,
                    )

        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados correctamente.'))
