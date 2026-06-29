import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum


class Community(models.Model):
    class Province(models.TextChoices):
        SALTA = 'Salta', 'Salta'
        JUJUY = 'Jujuy', 'Jujuy'
        CHACO = 'Chaco', 'Chaco'
        FORMOSA = 'Formosa', 'Formosa'

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='community_profile',
        verbose_name='usuario responsable',
        null=True,
        blank=True,
    )
    name = models.CharField('nombre', max_length=200)
    description = models.TextField('descripción')
    province = models.CharField('provincia', max_length=50, choices=Province.choices)
    population = models.PositiveIntegerField('población')
    email = models.EmailField('email de contacto')
    image = models.ImageField('imagen', upload_to='communities/', blank=True, null=True)
    image_url = models.URLField('URL de imagen', blank=True)
    is_active = models.BooleanField('activa', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comunidad'
        verbose_name_plural = 'comunidades'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return '/static/img/comunidad-default.svg'

    @property
    def active_needs_count(self):
        return self.needs.filter(status=Need.Status.ACTIVE).count()

    @property
    def urgent_needs_count(self):
        return self.needs.filter(status=Need.Status.ACTIVE, is_urgent=True).count()


class Need(models.Model):
    class Category(models.TextChoices):
        ALIMENTOS = 'Alimentos', 'Alimentos'
        SALUD = 'Salud', 'Salud'
        EDUCACION = 'Educación', 'Educación'
        VIVIENDA = 'Vivienda', 'Vivienda'
        OTRO = 'Otro', 'Otro'

    class Status(models.TextChoices):
        ACTIVE = 'activa', 'Activa'
        COMPLETED = 'completada', 'Completada'
        CANCELLED = 'cancelada', 'Cancelada'

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='needs',
        verbose_name='comunidad',
    )
    title = models.CharField('título', max_length=200)
    description = models.TextField('descripción')
    category = models.CharField('categoría', max_length=50, choices=Category.choices)
    target_amount = models.DecimalField('monto objetivo', max_digits=12, decimal_places=2)
    is_urgent = models.BooleanField('urgente', default=False)
    status = models.CharField(
        'estado',
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'necesidad'
        verbose_name_plural = 'necesidades'
        ordering = ['-is_urgent', '-created_at']

    def __str__(self):
        return self.title

    @property
    def raised_amount(self):
        total = self.donations.aggregate(total=Sum('amount'))['total']
        return total or Decimal('0')

    @property
    def remaining_amount(self):
        return max(self.target_amount - self.raised_amount, Decimal('0'))

    @property
    def progress_percent(self):
        if self.target_amount <= 0:
            return 0
        percent = (self.raised_amount / self.target_amount) * 100
        return min(int(percent), 100)

    @property
    def is_funded(self):
        return self.raised_amount >= self.target_amount


class Donation(models.Model):
    need = models.ForeignKey(
        Need,
        on_delete=models.CASCADE,
        related_name='donations',
        verbose_name='necesidad',
    )
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations',
        verbose_name='donante',
    )
    amount = models.DecimalField('monto', max_digits=12, decimal_places=2)
    confirmation_code = models.CharField('código de confirmación', max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'donación'
        verbose_name_plural = 'donaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.confirmation_code} - ${self.amount}'

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = self.generate_code()
        super().save(*args, **kwargs)
        if self.need.is_funded and self.need.status == Need.Status.ACTIVE:
            self.need.status = Need.Status.COMPLETED
            self.need.save(update_fields=['status'])

    @staticmethod
    def generate_code():
        return f'DON-{uuid.uuid4().hex[:12].upper()}'
