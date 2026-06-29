from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'tu@email.com',
            'class': 'form-input',
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
        }),
    )

    error_messages = {
        'invalid_login': 'Email o contraseña incorrectos.',
        'inactive': 'Esta cuenta está desactivada.',
    }


class RegisterForm(forms.ModelForm):
    display_name = forms.CharField(
        label='Nombre',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre',
            'class': 'form-input',
        }),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'tu@email.com',
            'class': 'form-input',
        }),
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    account_type = forms.ChoiceField(
        label='Tipo de cuenta',
        choices=User.AccountType.choices,
        widget=forms.RadioSelect(),
        initial=User.AccountType.DONANTE,
    )

    class Meta:
        model = User
        fields = ('display_name', 'email', 'account_type')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este email.')
        return email

    def clean_password1(self):
        password = self.cleaned_data['password1']
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.display_name = self.cleaned_data['display_name']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
