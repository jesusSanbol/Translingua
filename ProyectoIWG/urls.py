from django.contrib import admin
from django.urls import path, re_path, include
from ProyectoIWG.views import home, tralin, traducir_archivo, mostrar_resultado, mis_archivos, eliminar_archivo
from django.contrib.auth import views as auth_views
from social_django import urls as social_auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('tliwg/', tralin),

    path('', traducir_archivo, name='traducir_archivo'),
    path('resultado/<int:pk>/', mostrar_resultado, name='resultado'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),

    path('mis_archivos/', mis_archivos, name='mis_archivos'),
    path('eliminar_archivo/<int:pk>/', eliminar_archivo, name='eliminar_archivo'),
]

