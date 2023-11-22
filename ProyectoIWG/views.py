from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ArchivoSTRForm
from traductor.models import ArchivoSTR
from google.cloud import translate_v2 as translate

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Redirigir a la página deseada después del inicio de sesión
            return redirect('traductor/traducir_archivo.htmll')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def home(request): 
    return HttpResponse("Translingua Project")

def tralin(request): 
    return HttpResponse("tceyorP augnilsnarT")

# Elimina la línea que importa 'django_ratelimit' ya que no la necesitarás

def traducir_archivo(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirige a la página de inicio de sesión si el usuario no está autenticado

    if request.method == 'POST':
        form = ArchivoSTRForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_str = form.save(commit=False)
            archivo_str.usuario = request.user  

            # Guardar el archivo
            archivo_str.save()

            # Traducción del archivo usando la Cloud Translation API
            target_language = request.POST.get('idioma_destino')  # Obtener el idioma seleccionado por el usuario

            # Configurar las credenciales de Google Cloud
            # Asegúrate de haber instalado la biblioteca de traducción: pip install google-cloud-translate
            # Además, configura tus credenciales de Google Cloud en tu entorno
            client = translate.Client()

            # Realiza la traducción
            result = client.translate(archivo_str.contenido, target_language=target_language)

            # Guardar la traducción en el modelo
            archivo_str.traduccion = result['input']
            archivo_str.save()

            # Después de guardar el archivo, redirige a la página de resultados
            return redirect('mostrar_resultado', pk=archivo_str.pk)
    else:
        form = ArchivoSTRForm()

    return render(request, 'traductor/traducir_archivo.html', {'form': form})

def mostrar_resultado(request, pk):
    archivo_str = get_object_or_404(ArchivoSTR, pk=pk)
    return render(request, 'traductor/resultado.html', {'archivo_str': archivo_str})

def mis_archivos(request):
    archivos = ArchivoSTR.objects.filter(usuario=request.user)
    return render(request, 'traductor/mis_archivos.html', {'archivos': archivos})

def eliminar_archivo(request, pk):
    archivo = get_object_or_404(ArchivoSTR, pk=pk)
    if request.method == 'POST':
        archivo.delete()
        return redirect('mis_archivos')
    return render(request, 'traductor/eliminar_archivo.html', {'archivo': archivo})

