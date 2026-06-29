from django.conf import settings
from django.db import models


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'abierto', 'Abierto'
        IN_PROGRESS = 'en_progreso', 'En progreso'
        RESOLVED = 'resuelto', 'Resuelto'
        CLOSED = 'cerrado', 'Cerrado'

    class Priority(models.TextChoices):
        LOW = 'baja', 'Baja'
        MEDIUM = 'media', 'Media'
        HIGH = 'alta', 'Alta'
        URGENT = 'urgente', 'Urgente'

    class Category(models.TextChoices):
        GENERAL = 'general', 'General'
        DONATION = 'donacion', 'Donación'
        COMMUNITY = 'comunidad', 'Comunidad'
        TECHNICAL = 'tecnico', 'Técnico'
        OTHER = 'otro', 'Otro'

    title = models.CharField('título', max_length=200)
    description = models.TextField('descripción')
    category = models.CharField('categoría', max_length=20, choices=Category.choices, default=Category.GENERAL)
    priority = models.CharField('prioridad', max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField('estado', max_length=20, choices=Status.choices, default=Status.OPEN)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_created',
        verbose_name='creado por',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_assigned',
        verbose_name='asignado a',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.pk} - {self.title}'


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments', verbose_name='ticket')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ticket_comments',
        verbose_name='autor',
    )
    content = models.TextField('comentario')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'
        ordering = ['created_at']

    def __str__(self):
        return f'Comentario en #{self.ticket_id}'
