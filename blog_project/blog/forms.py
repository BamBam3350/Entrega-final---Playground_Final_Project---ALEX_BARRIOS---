from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in password1):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not any(char.isalpha() for char in password1):
            raise ValidationError("La contraseña debe contener al menos una letra.")
        
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        
        return password2
    
    def clean_username(self):
        username = self.cleaned_data['username']
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'biography', 'birthday']

    def clean_biography(self):
        biography = self.cleaned_data.get('biography')
        if biography and len(biography) > 500:
            raise forms.ValidationError("La biografía es demasiado larga.")
        return biography
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024: 
                raise forms.ValidationError("La imagen es demasiado grande. El tamaño máximo permitido es 5 MB.")
            if not avatar.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Por favor, suba una imagen en formato PNG, JPG o JPEG.")
        return avatar
