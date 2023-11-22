from django.db import models
from django.contrib.auth.models import User


class ArchivoSTR(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='archivos_str/')
    idioma_destino = models.CharField(max_length=10)
    traduccion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

