from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages import constants as messages
from .forms import CustomUserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
import os

def index(request):
    """
    Muestra la página principal con las pestañas de Sign Up y Log In.
    """
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, 'base.html')

@login_required
def main(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # La contraseña se guarda de forma segura usando set_password internamente.
            # Renderizamos una plantilla que muestra el mensaje y redirige a dashboard.
            return render(request, 'main.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if login(request, user):
                return redirect("main")
            elif not user.is_active:
                messages.error(request, "Tu cuenta ha sido desactivada.")

    if request.user.is_authenticated:
        return redirect("main")
    else:
        return render(request, "index.html")




def user_logout(request):
    """
    Cierra sesión del usuario.
    """
    logout(request)
    return redirect('login')


def face(request):
    """
    Muestra la página principal con las pestañas de Sign Up y Log In.
    """
    return render(request, 'face.html')

def sede(request):
    """
    Muestra la página principal con las pestañas de Sign Up y Log In.
    """
    return render(request, 'sede.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import UserUpload
from .utils.functions import remitir_en_FACE  # ✅ Importamos la función de Selenium

import os


def face_upload(request):
    if request.method == 'POST':
        print("🟢 Se recibió una solicitud POST en /face_upload/")  # ✅ Verifica que llega el request

        xml_files = request.FILES.getlist('xml_files')
        pdf_files = request.FILES.getlist('pdf_files')
        email = request.POST.get('email', 'test@example.com')  # Email ingresado en el formulario

        print(f"📩 Email recibido: {email}")
        print(f"📂 {len(xml_files)} archivos XML recibidos.")
        print(f"📂 {len(pdf_files)} archivos PDF recibidos.")

        # 📂 **Ruta absoluta para guardar archivos**
        upload_dir = os.path.join(settings.BASE_DIR, "uploads/")
        os.makedirs(upload_dir, exist_ok=True)  # Crea la carpeta si no existe
        print(f"📁 Directorio de subida: {upload_dir}")

        xml_paths = []
        pdf_paths = []

        # ✅ **Guardar archivos y obtener rutas absolutas**
        for file in xml_files:
            xml_path = os.path.join(upload_dir, file.name)
            with open(xml_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            xml_paths.append(xml_path)  # Guarda la ruta
            UserUpload.objects.create(xml_firmado=file)
            print(f"✅ XML guardado: {xml_path}")

        for file in pdf_files:
            pdf_path = os.path.join(upload_dir, file.name)
            with open(pdf_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            pdf_paths.append(pdf_path)  # Guarda la ruta
            UserUpload.objects.create(pdf=file)
            print(f"✅ PDF guardado: {pdf_path}")

        # ✅ **Pasar rutas absolutas a Selenium llamando a `functions.py`**
        if xml_paths:  # Solo ejecuta Selenium si hay un XML
            print("🚀 Ejecutando Selenium para remitir facturas...")
            selenium_result = remitir_en_FACE(upload_dir, email)
        else:
            selenium_result = "❌ No se subió ningún archivo XML."
            print(selenium_result)

        print("✅ Proceso de remisión finalizado.")

        # 🔴 BORRAMOS LOS ARCHIVOS AL FINAL DEL PROCESO 🔴
        for path in xml_paths:
            if os.path.exists(path):
                os.remove(path)
                print(f"🗑️ Archivo eliminado: {path}")
                # ademas de xml_firmado, se elimina el pdf
                UserUpload.objects.filter(xml_firmado=path).delete()

        for path in pdf_paths:
            if os.path.exists(path):
                os.remove(path)
                print(f"🗑️ Archivo eliminado: {path}")
                # ademas de pdf, se elimina el xml_firmado
                UserUpload.objects.filter(pdf=path).delete()
            

        return JsonResponse({"message": "Archivos subidos correctamente.", "selenium": selenium_result})

    return render(request, 'face_upload.html')

def base(request):
    return render(request, 'base.html')

def exito(request):
    return render(request, 'exito.html')
# Compare this snippet from Tabellarius/AutoFACe/views.py:
