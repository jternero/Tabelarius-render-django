"""
URL configuration for Tabellarius project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from AutoFACe.views import index, login_view, register, user_logout, main, face, sede, face_upload, exito
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),            # Página principal con pestañas
    path('register/', register, name='register'),  # Procesa el registro
    path('login/', login_view, name='login'),      # Procesa el login
    path('logout/', user_logout, name='logout'),   # Cierra sesión
    path('main/', main, name='main'),              # Página principal del usuario
    path('face/', face, name='face'),              # Página principal del usuario
    path('sede/', sede, name='sede'),              # Página principal del usuario
    path('face_upload/', face_upload, name='face_upload'),
    path('exito/', lambda request: render(request, 'exito.html'), name='exito'),

]

<<<<<<< HEAD
#if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, "staticfiles"))
=======
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, "../staticfiles"))
>>>>>>> 80090b5 (Render fixes 3)
