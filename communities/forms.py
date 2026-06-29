from django import forms

from .models import Need


class NeedForm(forms.ModelForm):
    class Meta:
        model = Need
        fields = ('title', 'description', 'category', 'target_amount', 'is_urgent')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Alimentos no perecederos para el invierno',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe en detalle la necesidad y cómo se utilizarán los fondos...',
                'rows': 4,
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'target_amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '50000',
                'min': '1',
                'step': '1',
            }),
            'is_urgent': forms.CheckboxInput(attrs={'class': 'toggle-input'}),
        }
        labels = {
            'title': 'Título de la necesidad',
            'description': 'Descripción',
            'category': 'Categoría',
            'target_amount': 'Monto objetivo (ARS)',
            'is_urgent': 'Marcar como urgente',
        }


class DonationForm(forms.Form):
    amount = forms.DecimalField(
        label='Monto a donar (ARS)',
        min_value=1,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-input form-input-lg',
            'placeholder': '10000',
        }),
    )
