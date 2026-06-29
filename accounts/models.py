from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class AccountType(models.TextChoices):
        DONANTE = 'donante', 'Donante'
        COMUNIDAD = 'comunidad', 'Comunidad'

    display_name = models.CharField('nombre', max_length=150, blank=True)
    account_type = models.CharField(
        'tipo de cuenta',
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.DONANTE,
    )

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def get_display_name(self):
        return self.display_name or self.username

    @property
    def is_community(self):
        return self.account_type == self.AccountType.COMUNIDAD

    @property
    def is_donor(self):
        return self.account_type == self.AccountType.DONANTE

    @property
    def avatar_initial(self):
        name = self.get_display_name()
        return name[0].upper() if name else 'U'
