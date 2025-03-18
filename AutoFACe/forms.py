# AutoFACe/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text="Requerido. Ingresa una dirección de correo válida."
    )
    first_name = forms.CharField(
        required=True, 
        max_length=30, 
        help_text="Requerido. Tu nombre."
    )
    last_name = forms.CharField(
        required=True, 
        max_length=30, 
        help_text="Requerido. Tus apellidos."
    )

    class Meta:
        model = User
        fields = (
            "username", 
            "email", 
            "first_name", 
            "last_name", 
            "password1", 
            "password2"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

# forms.py
from django import forms
from .models import UserUpload

class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields = ['email', 'xml_firmado', 'pdf']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not (file.name.endswith('.pdf') or file.name.endswith('.xml_signed.xsig')):
            raise forms.ValidationError("Sólo se permiten archivos PDF y XML.")
        elif file.size > 10*1024*1024:
            raise forms.ValidationError("El archivo es demasiado grande. El tamaño máximo permitido es de 10MB.")
        elif file.name.endswith('.pdf') and file.size > 5*1024*1024:
            raise forms.ValidationError("Los archivos PDF no pueden superar los 5MB.")
        elif file.name.endswith('.xml_signed.xsig') and file.size > 6*1024*1024:
            raise forms.ValidationError("Los archivos XML firmados no pueden superar los 6MB.")
        elif file.name.endswith('.xml_signed.xsig') != file.name.endswith('.pdf'):
            raise forms.ValidationError("Los archivos deben tener los mismos nombres base.")

        return file
    
